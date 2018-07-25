import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)


for i in range(arg1):
    ORDER66 += "-o orderer" + str(i) + ".example.com:7050 --cafile /etc/hyperledger/msp/orderer" + str(i) + "/msp/tlscacerts/tlsca.example.com-cert.pem "
    
file = """
# Create the channel
docker exec peer0.org1.example.com peer channel create -c composerchannel --tls -f /etc/hyperledger/configtx/composer-channel.tx""" + ORDER66 + """

echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}

docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" root.org1.example.com peer channel join -b composerchannel.block --tls --cafile /etc/hyperledger/msp/orderer0/msp/tlscacerts/tlsca.example.com-cert.pem
"""

text_file = open("bootstrap.sh", "w")
text_file.write(file)
text_file.close()