import pytest


@pytest.fixture
def asset():
    return {
        'agent_names': [],
        'agent_uuid': None,
        'aws_availability_zone': None,
        'aws_ec2_instance_ami_id': None,
        'aws_ec2_instance_group_name': None,
        'aws_ec2_instance_id': None,
        'aws_ec2_instance_state_name': None,
        'aws_ec2_instance_type': None,
        'aws_ec2_name': None,
        'aws_ec2_product_code': None,
        'aws_owner_id': None,
        'aws_region': None,
        'aws_subnet_id': None,
        'aws_vpc_id': None,
        'azure_resource_id': None,
        'azure_vm_id': None,
        'bios_uuid': 'e1d10a2d-4940-04f5-7970-0cd1f20ab930',
        'created_at': '2019-03-04T22:13:44.642Z',
        'deleted_at': None,
        'deleted_by': None,
        'first_scan_time': '2019-03-05T23:26:05.569Z',
        'first_seen': '2019-03-04T22:13:44.589Z',
        'fqdns': ['ip-10-128-0-2.ec2.internal'],
        'gcp_instance_id': '1644712871559487695',
        'gcp_project_id': 'example-233118',
        'gcp_zone': 'us-central1-c',
        'has_agent': False,
        'has_plugin_results': True,
        'hostnames': ['instance-1'],
        'id': '7c8053c6-3205-4322-a746-d263f7356eb7',
        'ipv4s': ['35.222.103.145', '10.128.0.2'],
        'ipv6s': [],
        'last_authenticated_scan_date': '2019-03-05T23:26:05.569Z',
        'last_licensed_scan_date': '2019-03-05T23:26:05.569Z',
        'last_scan_time': '2019-03-05T23:26:05.569Z',
        'last_seen': '2019-03-10T22:14:15.329Z',
        'mac_addresses': ['42:01:0a:80:00:02'],
        'manufacturer_tpm_ids': [],
        'mcafee_epo_agent_guid': None,
        'mcafee_epo_guid': None,
        'netbios_names': ['instance-1'],
        'network_id': None,
        'network_interfaces': [
            {
                'aliased': None,
                'fqdns': [],
                'ipv4s': [],
                'ipv6s': [],
                'mac_addresses': [],
                'name': 'nic0',
                'virtual': True
            }
        ],
        'network_name': None,
        'operating_systems': ['debian-9-stretch'],
        'qualys_asset_ids': [],
        'qualys_host_ids': [],
        'servicenow_sysid': None,
        'sources': [
            {
                'first_seen': '2019-03-04T22:13:44.589Z',
                'last_seen': '2019-03-10T22:14:15.329Z',
                'name': 'GCP'
            }, {
                'first_seen': '2019-03-05T23:26:05.569Z',
                'last_seen': '2019-03-05T23:26:05.569Z',
                'name': 'NESSUS_SCAN'
            }
        ],
        'ssh_fingerprints': [],
        'symantec_ep_hardware_keys': [],
        'system_types': ['gcp-instance'],
        'tags': [],
        'terminated_at': None,
        'terminated_by': None,
        'updated_at': '2019-03-10T22:14:15.427Z'
    }