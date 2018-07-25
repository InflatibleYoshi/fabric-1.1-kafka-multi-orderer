import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

HOSTS = ""
CONFIGTX = ""
CRYPTOCONFIG  = ""
PEERNUMBER = ""
PEERADMINCARD = ""
for i in range(arg1):
    HOSTS += 'HOST' + str(i+1) + '=192.168.1.' + str(i+5) + '\n'

for i in range(arg1):
    CONFIGTX += 'sed -i -e "s/{IP-HOST-' + str(i+1) + '}/$HOST' + str(i+1) + '/g" configtx.yaml\n'

for i in range(arg1):
    CRYPTOCONFIG += 'sed -i -e "s/{IP-HOST-' + str(i+1) + '}/$HOST' + str(i+1) + '/g" crypto-config.yaml\n'

for i in range(arg1):
    PEERNUMBER += 'sed -i -e "s/{IP-HOST-1}/$HOST1/g" docker-compose-peer' + str(i+1) + '.yml\n'
    PEERNUMBER += 'sed -i -e "s/{IP-HOST-' + str(i+1) + '}/$HOST' + str(i+1) + '/g" docker-compose-peer' + str(i+1) + '.yml\n'

for i in range(arg1):
    PEERADMINCARD += 'sed -i -e "s/{IP-HOST-' + str(i+1) + '}/$HOST' + str(i+1) + '/g" ../createPeerAdminCard.sh\n'

file = """#!/bin/bash
cd "$(dirname "$0")"
HOST0=192.168.1.5
""" + HOSTS + """
""" + CONFIGTX + """
""" + CRYPTOCONFIG + """
""" + PEERNUMBER + """
""" + PEERADMINCARD + """

cryptogen generate --config=./crypto-config.yaml
export FABRIC_CFG_PATH=$PWD
configtxgen -profile ComposerOrdererGenesis -outputBlock ./composer-genesis.block
configtxgen -profile ComposerChannel -outputCreateChannelTx ./composer-channel.tx -channelID composerchannel

ORG1KEY="$(ls crypto-config/peerOrganizations/org1.example.com/ca/ | grep 'sk$')"

sed -i -e "s/{ORG1-CA-KEY}/$ORG1KEY/g" docker-compose.yml
"""

text_file = open("composer/howtobuild.sh", "w")
text_file.write(file)
text_file.close()