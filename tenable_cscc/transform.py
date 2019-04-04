from .cscc import SecurityCommandCenter, AlreadyExistsError
from .pool import ThreadPool
import logging, arrow, hashlib, time


def md5sum(*values):
    '''
    Creates an md5sum of a given list of strings, and returns the md5sum.
    
    Args:
        *values (str): A string to hash
    '''
    h = hashlib.md5()
    for v in values:
        h.update(v.encode('utf-8'))
    return h.hexdigest()


def trunc(text, limit):
    '''
    Truncates a string to a given number of characters.  If a string extends
    beyond the limit, then truncate and add an ellipses after the truncation.

    Args:
        text (str): The string to truncate
        limit (int): The maximum limit that the string can be.
    
    Returns:
        str: The truncated string
    '''
    if len(text) >= limit:
        return '{}...'.format(text[:limit - 4])
    return text


class GoogleSCCIngest:
    _assets = dict()

    def __init__(self, tio, gcp):
        self._log = logging.getLogger('{}.{}'.format(
            self.__module__, self.__class__.__name__))
        self.gcp = gcp
        self.tio = tio
    
    def _cache_asset(self, asset):
        '''
        Caches the asset resource path using the asset uuid as the key.

        Args:
            asset (dict): The Asset dictionary from Tenable.io
        '''
        self._assets[asset['id']] = ''.join([
            '//compute.googleapis.com'
            '/projects/{}'.format(asset.get('gcp_project_id')),
            '/zones/{}'.format(asset.get('gcp_zone')),
            '/instances/{}'.format(asset.get('gcp_instance_id'))
        ])
    
    def _transform_vulnerability(self, vuln):
        '''
        Transforms a Tenable.io vulnerability into a Google Cloud Security
        Command Center Finding. 

        Args:
            vuln (dict): The Tenable.io vulnerability
        
        Returns:
            str, dict: The GCP SCC Finding ID and the Finding document.
        '''
        state = {
            'OPEN': 'ACTIVE',
            'NEW': 'ACTIVE',
            'REOPENED': 'ACTIVE',
            'FIXED': 'INACTIVE'
        }
        fid = md5sum(
            vuln.get('asset').get('uuid'), 
            str(vuln.get('plugin').get('id')),
            str(vuln.get('port').get('port')),
            vuln.get('port').get('protocol')
        )
        plugin = vuln.get('plugin')
        return fid, {
            'name': '{}/findings/{}'.format(self.gcp.source_id, fid),
            'parent': self.gcp.source_id,
            'resourceName': self._assets[vuln.get('asset').get('uuid')],
            'state': state[vuln['state']],
            'category': plugin.get('name'),
            'externalUri': ''.join([
                'https://cloud.tenable.com/app.html#/dashboards/workbench',
                'assets/{}'.format(vuln.get('asset').get('id')),
                '/vulnerabilities/{}'.format(plugin.get('id'))
            ]),
            'sourceProperties': {
                'cves': ','.join(plugin.get('cve', [])),
                'cpes': ','.join(plugin.get('cpe', [])),
                'cvss_base_score': plugin.get('cvss_base_score', 'N/A'),
                'cvss_temporal_score': plugin.get('cvss_temporal_score', 'N/A'),
                'description': plugin.get('description'),
                'family': plugin.get('family'),
                'has_patch': plugin.get('has_patch'),
                'name': plugin.get('name'),
                'output': vuln.get('output', ''),
                'risk_factor': plugin.get('risk_factor'),
                'see_also': '|'.join(plugin.get('see_also', [])),
                'solution': plugin.get('solution'),
                'synopsis': plugin.get('synopsis'),
                'port': vuln.get('port').get('port'),
                'first_found': vuln.get('first_found'),
                'last_found': vuln.get('last_found')  
            },
            'eventTime': arrow.utcnow().isoformat(),
            'createTime': arrow.utcnow().isoformat()
        }
    
    def ingest(self, observed_since, batch_size=100, threads=2):
        '''
        Perform the ingestion

        Args:
            observed_since (int): 
                The unix timestamp of the age threshhold.  Only vulnerabilities
                observed since this date will be imported.
            batch_size (int, optional):
                The number of findings to send to SCC at a time.  If nothing is 
                specified, it will default to 100.
            threads (int, optional):
                The number of concurrent threads to insert the data into SCC.
                If nothing is specified, the default is 2
        '''
        # The first thing that we need to do is perform the asset resource
        # generation.  We will export all of the assets that have data from the
        # GCP connector and process that information to build the cache that we
        # will need for the vuln ingestion.
        self._log.info('generating asset resource records')
        assets = self.tio.exports.assets(sources=['GCP'], 
            updated_at=observed_since)
        for asset in assets:
            self._cache_asset(asset)
        self._log.info('discovered {} GCP assets'.format(len(self._assets)))

        # Now we need to  transform the vulnerability data.  We will initiate an
        # export of the vulnerabilities from Tenable.io.  If the vulnerability
        # pertains to a GCP asset, then we will transform that finding and
        # upsert the finding into GCP SCC.
        openvulns = self.tio.exports.vulns(last_updated=observed_since, 
            severity=['low', 'medium', 'high', 'critical'],
            state=['open', 'reopened'])
        fixedvulns = self.tio.exports.vulns(last_fixed=observed_since,
            severity=['low', 'medium', 'high', 'critical'],
            state=['fixed'])

        vcounter = 0
        pool = ThreadPool(threads)
        for state in [openvulns, fixedvulns]:
            for vuln in state:
                if vuln.get('asset').get('uuid') in self._assets.keys():
                    vcounter += 1
                    fid, finding = self._transform_vulnerability(vuln)
                    pool.add_task(self._upsert_finding, fid, finding)
        pool.wait_completion()
        self._log.info('transformed and ingested {} vulns'.format(vcounter))
    
    def _upsert_finding(self, fid, finding):
        try:
            self.gcp.findings.upsert(fid, finding)
        except AlreadyExistsError as err:
            self._log.debug('409 response for body={}'.format(finding))