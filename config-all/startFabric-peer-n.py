import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)
arg1 -= 1

for i in range(arg1):
    file = """#!/bin/bash

if [ -z ${FABRIC_START_TIMEOUT+x} ]; then
 echo "FABRIC_START_TIMEOUT is unset, assuming 15 (seconds)"
 export FABRIC_START_TIMEOUT=15
else

   re='^[0-9]+$'
   if ! [[ $FABRIC_START_TIMEOUT =~ $re ]] ; then
      echo "FABRIC_START_TIMEOUT: Not a number" >&2; exit 1
   fi

 echo "FABRIC_START_TIMEOUT is set to '$FABRIC_START_TIMEOUT'"
fi

# Exit on first error, print all commands.
set -ev

#Detect architecture
ARCH=`uname -m`

# Grab the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#

# ARCH=$ARCH docker-compose -f "${DIR}"/composer/docker-compose-peer""" + str(i + 2) + """.yml down
ARCH=$ARCH docker-compose -f "${DIR}"/composer/docker-compose-peer""" + str(i + 2) + """.yml up -d

# wait for Hyperledger Fabric to start
# incase of errors when running later commands, issue export FABRIC_START_TIMEOUT=<larger number>
echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}

docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer""" + str(i + 2) + """.org1.example.com peer channel fetch config -o orderer0.example.com:7050 -c composerchannel --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem

docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer""" + str(i + 2) + """.org1.example.com peer channel join -b composerchannel_config.block --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem

docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer""" + str(i + 3) + """.org1.example.com peer channel fetch config -o orderer0.example.com:7050 -c composerchannel --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem

docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer""" + str(i + 3) + """.org1.example.com peer channel join -b composerchannel_config.block --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem
"""

    text_file = open("startFabric-Peer" + str(i + 2) + ".sh", "w")
    text_file.write(file)
    text_file.close()