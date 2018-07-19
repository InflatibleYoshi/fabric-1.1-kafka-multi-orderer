import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

HOSTS = ""
CONFIGTX = ""
CRYPTOCONFIG  = ""
PEERNUMBER = ""
PEERADMINCARD = ""
arg1 -= 1
for i in range(arg1):
    HOSTS += 'HOST' + str(i+2) + '=\n'

for i in range(arg1):
    CONFIGTX += 'sed -i -e "s/$HOST' + str(i+2) + '/{IP-HOST-' + str(i+2) + '}/g" configtx.yaml\n'

for i in range(arg1):
    CRYPTOCONFIG += 'sed -i -e "s/$HOST' + str(i+2) + '/{IP-HOST-' + str(i+2) + '}/g" crypto-config.yaml\n'

for i in range(arg1):
    PEERNUMBER += 'sed -i -e "s/$HOST1/{IP-HOST-1}/g" docker-compose-peer' + str(i+2) + '.yaml\n'

for i in range(arg1):
    PEERADMINCARD += 'sed -i -e "s/$HOST' + str(i+2) + '/{IP-HOST-' + str(i+2) + '}/g" ../createPeerAdminCard.sh\n'

file = """#!/bin/bash
cd "$(dirname "$0")"
HOST1=
""" + HOSTS + """
sed -i -e "s/$HOST1/{IP-HOST-1}/g" configtx.yaml
""" + CONFIGTX + """
sed -i -e "s/$HOST1/{IP-HOST-1}/g" crypto-config.yaml
""" + CRYPTOCONFIG + """
sed -i -e "s/$HOST1/{IP-HOST-1}/g" docker-compose.yml
""" + PEERNUMBER + """
sed -i -e "s/$HOST1/{IP-HOST-1}/g" ../createPeerAdminCard.sh
""" + PEERADMINCARD + """

ORG1KEY="$(ls crypto-config/peerOrganizations/org1.example.com/ca/ | grep 'sk$')"

sed -i -e "s/$ORG1KEY/{ORG1-CA-KEY}/g" docker-compose.yml

rm -rf composer* crypto-config
"""

text_file = open("composer/howtorevert.sh", "w")
text_file.write(file)
text_file.close()