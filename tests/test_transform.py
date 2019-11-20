import pytest, os

def test_asset_cache(tio2scc, asset):
    tio2scc._cache_asset(asset)
    assert asset['id'] in tio2scc._assets
    assert tio2scc._assets[asset['id']] == '//compute.googleapis.com/projects/example-233118/zones/us-central1-c/instances/1644712871559487695'

def test_vuln_transform(tio2scc, asset, vuln):
    tio2scc._cache_asset(asset)
    fid, finding = tio2scc._transform_vulnerability(vuln)
    assert fid == 'bbdeb8235812830d977a74391ed59e70'
    assert finding ==  {
        'category': 'Linux Daemons with Broken Links to Executables',
        'createTime': finding['createTime'],
        'eventTime': finding['eventTime'],
        'externalUri': 'https://cloud.tenable.com/app.html#/dashboards/workbenchassets/None/vulnerabilities/44657',
        'name': 'organizations/981834921564/sources/11366567746046043010/findings/bbdeb8235812830d977a74391ed59e70',
        'parent': 'organizations/981834921564/sources/11366567746046043010',
        'resourceName': '//compute.googleapis.com/projects/example-233118/zones/us-central1-c/instances/1644712871559487695',
        'sourceProperties': {
            'cpes': '',
            'cves': '',
            'cvss_base_score': 10.0,
            'cvss_temporal_score': 'N/A',
            'description': '\n'.join([
                'By examining the \'/proc\' filesystem on the remote Linux host, Nessus',
                'has identified at least one currently-running daemon for which the',
                'link to the corresponding executable is broken.\n'
                'This can occur when the executable associated with a daemon is',
                'replaced on disk but the daemon itself has not been restarted.  And if',
                'the changes are security-related, the system may remain vulnerable to',
                'attack until the daemon is restarted.\n',
                'Alternatively, it could result from an attacker removing files in an',
                'effort to hide malicious activity.',
            ]),
            'family': 'Misc.',
            'has_patch': False,
            'name': 'Linux Daemons with Broken Links to Executables',
            'output': '\n'.join([
                'The following daemon is associated with a broken link to an\n=executable :'
                '\n  - 8834 tcp: (/opt/nessus/var/nessus/tmp/nessusd-old-2020170077)\n',
            ]),
            'port': 0,
            'risk_factor': 'Critical',
            'see_also': '',
            'solution': '\n'.join([
                'Inspect each reported daemon to determine why the link to the',
                'executable is broken.'
            ]),
            'synopsis': 'A daemon on the remote Linux host may need to be restarted.',
            'first_found': '2019-03-05T23:26:05.569Z',
            'last_found': '2019-03-05T23:26:05.569Z',
            'vpr_score': 'N/A',
        },
        'state': 'ACTIVE'
    }

@pytest.mark.vcr
@pytest.mark.skip(reason='Actual Ingestion requires maintained data.')
def test_ingest(tio2scc):
    tio2scc.ingest(0)