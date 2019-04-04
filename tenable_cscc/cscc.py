from tenable.base import APISession, APIEndpoint, APIResultsIterator
from tenable.errors import *
from google.oauth2 import service_account
from google.auth.transport import requests
import arrow


class AlreadyExistsError(APIError):
    pass


class SecurityCommandCenterIterator(APIResultsIterator):
    '''
    A simple iterator for SCC endpoints. Google seems to be implementing a
    "roll forward" mentality to paging by using a page token to denote the
    current state within the stack of data.
    '''
    _token = None
    _page_size = 1000
    _resource = None

    def _get_page(self):
        params = dict(pageSize=self._page_size)

        # if there is a page token already set, then we will use that for the
        # next call.
        if self._token:
            params['pageToken'] = self._token
        
        # perform the call & get the page & page token.
        resp = self._api.get(self._url, params=params).json()
        self._token = resp.get('nextPageToken')
        self.page = resp.get(self._resource, list())

        # not all API responses seem to have the totalSize attribute, so we will
        # first check to see if the attribute exists, and then degrade to using
        # the page of data returned to determine a more fuzzy total.
        if resp.get('totalSize'):
            self.total = resp['totalSize']
        elif len(self.page) == self._page_size:
            self.total = len(self.page) + 1
        else:
            self.total = len(self.page)


class SecurityCommandCenter(APISession):
    '''
    A minimal API class to handle authentication and the few API calls that we
    need for the integration.
    '''
    _url = 'https://securitycenter.googleapis.com/v1beta1'
    _scopes = ['https://www.googleapis.com/auth/cloud-platform']
    source_id = None
    _error_codes = {
        400: InvalidInputError,
        401: PermissionError,
        403: PermissionError,
        404: NotFoundError,
        409: AlreadyExistsError,
        500: ServerError,
    }

    def __init__(self, keyfile, source_id):
        creds = service_account.Credentials.from_service_account_file(keyfile)
        scoped = creds.with_scopes(self._scopes)
        session = requests.AuthorizedSession(scoped)
        self.source_id = source_id
        APISession.__init__(self, session=session)
    
    @property
    def findings(self):
        return SCCFindings(self)


class SCCFindings(APIEndpoint):
    def upsert(self, finding_id, finding, mask=None):
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
                'event_time',
                'source_properties.cvss_temporal_score',
                'source_properties.has_patch',
                'source_properties.output'
            ]
        
        return self._api.patch('{}/findings/{}'.format(
            self._api.source_id, finding_id), json=finding).json()

