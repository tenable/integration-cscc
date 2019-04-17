#!/bin/bash

# Install the prerequisites
apt -y install python3 python3-pip git

# Install the bridge
pip3 install tenable-cscc

# Construct the service file
cat <<'EOF' > /lib/systemd/system/tenable-cscc.service
[Unit]
Description=Tenable.io to CSCC Bridge
After=network.target

[Service]
Type=simple
EnvironmentFile=/etc/tenable-cscc.conf
ExecStart=/usr/local/bin/tenable-cscc
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Construct the environment file
cat <<'EOF' > /etc/tenable-cscc.conf
# The Tenable.io API Access and Secret Keys
# TIO_ACCESS_KEY="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
# TIO_SECRET_KEY="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
TIO_ACCESS_KEY=""
TIO_SECRET_KEY=""

# The Google Cloud Service Account file location.  This file should be the JSON
# document that informs the integration how to communicate to Google Cloud
# https://cloud.google.com/iam/docs/creating-managing-service-account-keys
CSCC_ACCOUNT_FILE="/etc/google-account.json"

# The Source ID that was generated from enabling the Tenable.io Security Source
# CSCC_SOURCE_ID="organizations/{ORGID}/sources/{SOURCEID}"
CSCC_SOURCE_ID=""

# How often should the bridge ingest data from Tenable.io.  This value is
# is specified in hours.
RUN_EVERY="24"

# How many threads should be used for pushing the data into CSCC?  The default
# value of 2 generally should be sufficient.
THREADS="2"
EOF

# Reload the Systemd daemon and enable the service
systemctl daemon-reload
systemctl enable tenable-cscc