# Tenable.io -> Google Security Command Center

This tool is designed to consume Tenable.io asset and vulnerability data,
transform that data into the Google Security Command Center format, and then 
upload the resulting data into Google Security Command Center.

The tool can be run as either a one-shot docker container or as a command-line
tool.  To run as a docker image, you'll need to build the image and then pass
the necessary secrets on to the container.

To run as a command-line tool, you'd need to install the required python modules
and then can run the tool using either environment variables or by passing the
required parameters as run-time parameters.

### Requirements for use

* API Keys for a service account in Tenable.io that can use the Exports API
  (Generally an Admin User)
* Service Account within Google Cloud that has the required permissions to
  edit findings and state (_Security Center Findings Editor_, and 
  _Security Center Findings State Setter_ roles).
* A host to run the script on that can run a Python 3.x environment.  As this
  bridge talks cloud-to-cloud, where it is located does not matter.


### Installing
```shell
pip install tenable-cscc
```

### Setup

1. Add the Tenable.io CSCC Service from the [Marketplace][marketplace]
2. Copy the source id that was generated (we will use this later)
3. [Create a service key][create_key] for the account that was created
4. Create a new VM Instance to store the integration (Debian 9)
5. Download the installation script: `curl -o installer.sh https://raw.githubusercontent.com/tenable/integrations-cscc/master/install-tenable-cscc.sh`
6. Run the installer `sudo installer.sh`
7. Copy the service key onto the host (such as /etc/google-account.json).
8. Update the variables within the /etc/conf.d/tenable-cscc file.
9. Start the service `systemctl start tenable-cscc`

### Options
The following below details both the command-line arguments as well as the 
equivalent environment variables.

```
Usage: tenable-cscc [OPTIONS]

  Tenable.io -> Google Cloud Security Command Center Bridge

Options:
  --tio-access-key TEXT           Tenable.io Access Key
  --tio-secret-key TEXT           Tenable.io Secret Key
  -b, --batch-size INTEGER        Export/Import Batch Sizing
  -v, --verbose                   Logging Verbosity
  -s, --observed-since INTEGER    The unix timestamp of the age threshold
  -r, --run-every INTEGER         How many hours between recurring imports
  -t, --threads INTEGER           How many concurrent threads to run for the
                                  import.
  -s, --service-account-file PATH
  -i, --service-id TEXT           The GCP CSCC Source ID
  --help                          Show this message and exit.
```

### Usage

Run the import once:

```
tenable-cscc                                    \
    --tio-access-key {TIO_ACCESS_KEY}           \
    --tio-secret-key {TIO_SECRET_KEY}           \
    --service-account-file {SA_JSON_FILENAME}   \
    --org-id {ORG_ID}
```

Run the import once an hour:

```
tenable-cscc                                    \
    --tio-access-key {TIO_ACCESS_KEY}           \
    --tio-secret-key {TIO_SECRET_KEY}           \
    --service-account-file {SA_JSON_FILENAME}   \
    --org-id {ORG_ID}
    --run-every 1
```

### Changelog
[Visit the CHANGELOG](CHANGELOG.md)

[marketplace]: https://console.cloud.google.com/security/command-center/dashboard?authuser=2&organizationId=981834921564&orgonly=true&supportedpurview=organizationId&subtask=browse&filter=category:security-command-center-services&subtaskIndex=1
[create_key]: https://cloud.google.com/iam/docs/creating-managing-service-account-keys
