import pytest, os, uuid
from tenable.io import TenableIO
from gcp_scc.scc import SecurityCommandCenter
from gcp_scc.transform import GoogleSCCIngest
from .fixture_asset import asset
from .fixture_vuln import vuln

@pytest.fixture
def scc(request, vcr):
    with vcr.use_cassette('gcp_scc_login'):
        return SecurityCommandCenter(
            os.getenv('SCC_KEYFILE', 'tests/test_files/keyfile.json'),
            os.getenv('SCC_ORG_ID', 981834921564))

@pytest.fixture
def tio(request, vcr):
    with vcr.use_cassette('tio_login'):
        return TenableIO()

@pytest.fixture
def tio2scc(scc, tio):
    return GoogleSCCIngest(tio, scc)