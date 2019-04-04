import pytest

@pytest.fixture
def vuln():
    return {
    'asset': {
        'bios_uuid': 'd151475c-297c-97b8-d790-8d6e9181985b',
        'device_type': 'general-purpose',
        'fqdn': 'localhost',
        'hostname': '127.0.0.1',
        'ipv4': '127.0.0.1',
        'last_authenticated_results': '2019-03-05T23:26:03Z',
        'mac_address': '42:01:0A:8E:00:02',
        'netbios_name': 'instance-2',
        'operating_system': [
            'Linux Kernel 3.10.0-957.5.1.el7.x86_64 on CentOS Linux release 7.6.1810 (Core)'],
        'tracked': True,
        'uuid': '7c8053c6-3205-4322-a746-d263f7356eb7'
    },
    'first_found': '2019-03-05T23:26:05.569Z',
    'last_found': '2019-03-05T23:26:05.569Z',
    'output': '\n'.join([
        'The following daemon is associated with a broken link to an\n=executable :'
        '\n  - 8834 tcp: (/opt/nessus/var/nessus/tmp/nessusd-old-2020170077)\n',
    ]),
    'plugin': {
        'cvss_base_score': 10.0,
        'cvss_vector': {
            'access_complexity': 'Low',
            'access_vector': 'Network',
            'authentication': 'None required',
            'availability_impact': 'Complete',
            'confidentiality_impact': 'Complete',
            'integrity_impact': 'Complete',
            'raw': 'AV:N/AC:L/Au:N/C:C/I:C/A:C'},
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
        'family_id': 23,
        'has_patch': False,
        'id': 44657,
        'modification_date': '2015-10-21T00:00:00Z',
        'name': 'Linux Daemons with Broken Links to Executables',
        'publication_date': '2010-02-17T00:00:00Z',
        'risk_factor': 'Critical',
        'solution': '\n'.join([
            'Inspect each reported daemon to determine why the link to the',
            'executable is broken.'
        ]),
        'synopsis': 'A daemon on the remote Linux host may need to be restarted.',
        'type': 'local',
        'version': '$Revision: 1.6 $'
    },
    'port': {'port': 0, 'protocol': 'TCP'},
    'scan': {
        'completed_at': '2019-03-05T23:26:05.569Z',
        'schedule_uuid': 'template-0997f4c5-7222-0e9a-4055-2323df3e123b26840e25d20c2285',
        'started_at': '2019-03-05T23:20:31.942Z',
        'uuid': '64e57f87-40b9-4154-9128-13f5121142ff'
    },
    'severity': 'critical',
    'severity_default_id': 4,
    'severity_id': 4,
    'severity_modification_type': 'NONE',
    'state': 'OPEN'}