


"""
# Create the channel
docker exec peer0.org1.example.com peer channel create -o orderer0.example.com:7050 -c composerchannel -f /etc/hyperledger/configtx/composer-channel.tx --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem

echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}

# Join peer0.org1.example.com to the channel.
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer0.org1.example.com peer channel join -b composerchannel.block --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem

# # Create the channel
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel fetch config -o orderer0.example.com:7050 -c composerchannel --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem
# docker exec peer1.org1.example.com peer channel create -o orderer.example.com:7050 -c composerchannel -f /etc/hyperledger/configtx/composer-channel.tx

# # Join peer1.org1.example.com to the channel.
docker exec -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org1.example.com/msp" peer1.org1.example.com peer channel join -b composerchannel_config.block --tls --cafile /etc/hyperledger/msp/orderer/msp/tlscacerts/tlsca.example.com-cert.pem
"""