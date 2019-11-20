import pytest, os, uuid
from tenable.io import TenableIO
from tenable_cscc.cscc import  SecurityCommandCenter
from tenable_cscc.transform import GoogleSCCIngest
from .fixture_asset import asset
from .fixture_vuln import vuln

@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [
            ('X-APIKeys', 'accessKey=TIO_ACCESS_KEY;secretKey=TIO_SECRET_KEY'),
            ('x-request-uuid', 'ffffffffffffffffffffffffffffffff'),
        ],
    }

@pytest.fixture
def scc(request, vcr):
    with vcr.use_cassette('gcp_scc_login'):
        return SecurityCommandCenter(
            os.getenv('SCC_KEYFILE', 'tests/test_files/keyfile.json'),
            os.getenv('SCC_SOURCE_ID', 'organizations/981834921564/sources/11366567746046043010'))

@pytest.fixture
def tio(request, vcr):
    return TenableIO(
        os.getenv('TIO_TEST_ACCESS_KEY'),
        os.getenv('TIO_TEST_SECRET_KEY'),
        vendor='pytest',
        product='tenable-cscc-automated-testing',
    )

@pytest.fixture
def tio2scc(scc, tio):
    return GoogleSCCIngest(tio, scc)