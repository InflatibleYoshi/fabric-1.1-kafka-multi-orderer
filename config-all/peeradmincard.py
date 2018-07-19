import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

ORDERERCA = ""
ORDERERS = ""
PEERS = ""
ORGPEERS = ""
ORDERERCONFIG = ""
PEERCONFIG = ""

arg1 -= 1

for i in range(arg1):
    ORDERERCA += """ORDERER""" + str(i+1) + """CA="$(awk 'NF {sub(/\\r/, ""); printf "%s\\\\n",$0;}' composer/crypto-config/ordererOrganizations/example.com/orderers/orderer""" + str(i + 1) + '.example.com/tls/ca.crt)"\n'
for i in range(arg1):
    ORDERERS += '                "orderer' + str(i + 1) + '.example.com",\n'
ORDERERS = ORDERERS[:-2]
for i in range(arg1 * 2):
    PEERS += '                "peer' + str(i + 2) + """.org1.example.com": {
                    "endorsingPeer": true,
                    "chaincodeQuery": true,
                    "eventSource": true
                },\n"""
PEERS = PEERS[:-2]
for i in range(arg1 * 2):
    ORGPEERS += '                "peer' + str(i + 2) + '.org1.example.com",\n'
ORGPEERS = ORGPEERS[:-2]

for i in range(arg1):
    ORDERERCONFIG += '        "orderer' + str(i + 1) + """.example.com":{ 
            "url": "grpcs://{IP-HOST-""" + str(i + 2) + """}:7050",
            "grpcOptions": {
                "ssl-target-name-override": "orderer""" + str(i + 1) + """.example.com"
            },
            "tlsCACerts": {
                "pem": "${ORDERER""" + str(i + 1) + """CA}"
            }
        },\n"""
ORDERERCONFIG = ORDERERCONFIG[:-2]

for i in range(arg1):
    PEERCONFIG += '        "peer' + str((i*2) + 2) + """.org1.example.com":{ 
            "url": "grpcs://{IP-HOST-""" + str(i + 2) + """}:9051",
            "eventUrl": "grpcs://{IP-HOST-""" + str(i + 2) + """}:9053",
            "grpcOptions": {
                "ssl-target-name-override": "peer""" + str((i*2) + 2) + """.org1.example.com"
            },
            "tlsCACerts": {
                "pem": "${ORG1CA}"
            }
        },
        "peer""" + str((i*2) + 3) + """.org1.example.com":{ 
            "url": "grpcs://{IP-HOST-""" + str(i + 2) + """}:10051",
            "eventUrl": "grpcs://{IP-HOST-""" + str(i + 2) + """}:10053",
            "grpcOptions": {
                "ssl-target-name-override": "peer""" + str((i*2) + 3) + """.org1.example.com"
            },
            "tlsCACerts": {
                "pem": "${ORG1CA}"
            }
        },\n"""

PEERCONFIG = PEERCONFIG[:-2]

file = """#!/bin/bash

# Exit on first error
set -e
# Grab the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Grab the file names of the keystore keys
ORG1KEY="$(ls composer/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/)"
ORDERER0CA="$(awk 'NF {sub(/\\r/, ""); printf "%s\\\\n",$0;}' composer/crypto-config/ordererOrganizations/example.com/orderers/orderer0.example.com/tls/ca.crt)"
""" + ORDERERCA + """
ORG1CA="$(awk 'NF {sub(/\\r/, ""); printf "%s\\\\n",$0;}' composer/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt)"

Parse_Arguments() {
	while [ $# -gt 0 ]; do
		case $1 in
			--help)
				HELPINFO=true
				;;
			--host | -h)
                shift
				HOST="$1"
				;;
            --noimport | -n)
				NOIMPORT=true
				;;
		esac
		shift
	done
}

HOST=localhost
Parse_Arguments $@

if [ "${HELPINFO}" == "true" ]; then
    Usage
fi

# Grab the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "${HL_COMPOSER_CLI}" ]; then
  HL_COMPOSER_CLI=$(which composer)
fi

echo
# check that the composer command exists at a version >v0.16
COMPOSER_VERSION=$("${HL_COMPOSER_CLI}" --version 2>/dev/null)
COMPOSER_RC=$?

if [ $COMPOSER_RC -eq 0 ]; then
    AWKRET=$(echo $COMPOSER_VERSION | awk -F. '{if ($2<19) print "1"; else print "0";}')
    if [ $AWKRET -eq 1 ]; then
        echo Cannot use $COMPOSER_VERSION version of composer with fabric 1.1, v0.19 or higher is required
        exit 1
    else
        echo Using composer-cli at $COMPOSER_VERSION
    fi
else
    echo 'No version of composer-cli has been detected, you need to install composer-cli at v0.19 or higher'
    exit 1
fi

cat << EOF > connection.json
{
    "name": "hlfv1",
    "x-type": "hlfv1",
    "x-commitTimeout": 300,
    "version": "1.0.0",
    "client": {
        "organization": "Org1",
        "connection": {
            "timeout": {
                "peer": {
                    "endorser": "300",
                    "eventHub": "300",
                    "eventReg": "300"
                },
                "orderer": "300"
            }
        }
    },
    "channels": {
        "composerchannel": {
            "orderers": [
                "orderer0.example.com",
""" + ORDERERS + """
            ],
            "peers": {
                "peer0.org1.example.com": {
                    "endorsingPeer": true,
                    "chaincodeQuery": true,
                    "eventSource": true
                },
                "peer1.org1.example.com": {
                    "endorsingPeer": true,
                    "chaincodeQuery": true,
                    "eventSource": true
                },\n""" + PEERS + """
            }
        }
    },
    "organizations": {
        "Org1": {
            "mspid": "Org1MSP",
            "peers": [
                "peer0.org1.example.com",
                "peer1.org1.example.com",
""" + ORGPEERS + """
            ],
            "certificateAuthorities": [
                "ca.org1.example.com"
            ]
        }
    },
    "orderers": {
        "orderer0.example.com": {
            "url": "grpcs://{IP-HOST-1}:7050",
            "grpcOptions": {
                "ssl-target-name-override": "orderer0.example.com"
            },
            "tlsCACerts": {
                "pem": "${ORDERER0CA}"
            }
        },
""" + ORDERERCONFIG + """
    },
    "peers": {
        "peer0.org1.example.com": {
            "url": "grpcs://{IP-HOST-1}:7051",
            "eventUrl": "grpcs://{IP-HOST-1}:7053",
            "grpcOptions": {
                "ssl-target-name-override": "peer0.org1.example.com"
            },
            "tlsCACerts": {
                "pem": "${ORG1CA}"
            }
        },
        "peer1.org1.example.com": {
            "url": "grpcs://{IP-HOST-1}:8051",
            "eventUrl": "grpcs://{IP-HOST-1}:8053",
            "grpcOptions": {
                "ssl-target-name-override": "peer1.org1.example.com"
            },
            "tlsCACerts": {
                "pem": "${ORG1CA}"
            }
        },
"""  + PEERCONFIG + """
    },
    "certificateAuthorities": {
        "ca.org1.example.com": {
            "url": "https://{IP-HOST-1}:7054",
            "caName": "ca.org1.example.com",
            "httpOptions": {
                "verify": false
            }
        }
    }
}
EOF

PRIVATE_KEY="${DIR}"/composer/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/"${ORG1KEY}"
CERT="${DIR}"/composer/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/Admin@org1.example.com-cert.pem

if [ "${NOIMPORT}" != "true" ]; then
    CARDOUTPUT=/tmp/PeerAdmin@hlfv1.card
else
    CARDOUTPUT=PeerAdmin@hlfv1.card
fi

"${HL_COMPOSER_CLI}"  card create -p connection.json -u PeerAdmin -c "${CERT}" -k "${PRIVATE_KEY}" -r PeerAdmin -r ChannelAdmin --file $CARDOUTPUT

if [ "${NOIMPORT}" != "true" ]; then
    if "${HL_COMPOSER_CLI}"  card list -c PeerAdmin@hlfv1 > /dev/null; then
        "${HL_COMPOSER_CLI}"  card delete -c PeerAdmin@hlfv1
    fi

    "${HL_COMPOSER_CLI}"  card import --file /tmp/PeerAdmin@hlfv1.card 
    "${HL_COMPOSER_CLI}"  card list
    echo "Hyperledger Composer PeerAdmin card has been imported, host of fabric specified as '${HOST}'"
    rm /tmp/PeerAdmin@hlfv1.card
else
    echo "Hyperledger Composer PeerAdmin card has been created, host of fabric specified as '${HOST}'"
fi
echo "Hyperledger Composer PeerAdmin card has been imported"
composer card list
"""

text_file = open("createPeerAdminCard.sh", "w")
text_file.write(file)
text_file.close()