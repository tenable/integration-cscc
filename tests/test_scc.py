import pytest

@pytest.fixture
def scc_finding():
    return {
        'category': 'example',
        'createTime': '2019-03-05T23:26:05.569Z',
        'eventTime': '2019-03-05T23:26:05.569Z',
        'externalUri': 'https://cloud.tenable.com/app.html#/dashboards/workbenchassets/None/vulnerabilities/44657',
        'name': 'organizations/981834921564/sources/2456454250925202170/findings/bbdeb8235812830d977a74391ed59e70',
        'parent': 'organizations/981834921564/sources/2456454250925202170',
        'resourceName': '/compute.googleapis.com/projects/example-233118/zones/us-central1-c/instances/1644712871559487695',
        'sourceProperties': {
            'cpes': '',
            'cves': '',
            'cvss_base_score': 10.0,
            'cvss_temporal_score': 'N/A',
        },
        'state': 'ACTIVE'
    }

@pytest.mark.vcr
def test_findings_upsert(scc, scc_finding):
    finding = scc.findings.upsert(scc_finding)