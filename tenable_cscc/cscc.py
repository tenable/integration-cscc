from restfly.session import APISession
from restfly.endpoint import APIEndpoint
from google.oauth2 import service_account
from google.auth.transport import requests
import arrow
from . import __version__


class SecurityCommandCenter(APISession):
    '''
    A minimal API class to handle authentication and the few API calls that we
    need for the integration.
    '''
    _url = 'https://securitycenter.googleapis.com/v1'
    _scopes = ['https://www.googleapis.com/auth/cloud-platform']
    _vendor = 'Tenable'
    _product = 'Google CSCC'
    _build = __version__
    source_id = None

    def __init__(self, keyfile, source_id, **kwargs):
        creds = service_account.Credentials.from_service_account_file(keyfile)
        scoped = creds.with_scopes(self._scopes)
        kwargs['session'] = requests.AuthorizedSession(scoped)
        self.source_id = source_id
        super(SecurityCommandCenter, self).__init__(**kwargs)

    @property
    def findings(self):
        return SCCFindings(self)


class SCCFindings(APIEndpoint):
    def upsert(self, finding, mask=None):
        '''
        Creates and/or updates the security finding.

        Args:
            finding_id (str): The resource id of the finding.
            finding (dict): The security finding document,
            mask (list, optional): The list of fields to update.

        Returns:
            dict: The security finding document.
        '''
        if not mask:
            mask = [
                'state',
                'eventTime',
                'sourceProperties.cvss_temporal_score',
                'sourceProperties.has_patch',
                'sourceProperties.output',
                'sourceProperties.vpr_score',
            ]

        return self._api.patch(finding['name'],
            json=finding,
            params={'updateMask': ','.join(mask)}
        ).json()

