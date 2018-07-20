import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

anchorPeers = ""
orderers  = ""
kafka = ""
arg1 -= 1
for i in range(arg1):
    anchorPeers += "            - Host: peer" + str( (i+1) * 2 ) + ".org1.example.com\n"
    anchorPeers += "            - Port: 9051\n"

for i in range(arg1):
    orderers += '        - {IP-HOST-' + str( (i+2)) + "}:7050\n"

for i in range(arg1):
    kafka += '            - {IP-HOST-' + str( (i+2)) + "}:9092\n"
    kafka += '            - {IP-HOST-' + str( (i+2)) + "}:10092\n"
    kafka += '            - {IP-HOST-' + str( (i+2)) + "}:11092\n"
    kafka += '            - {IP-HOST-' + str( (i+2)) + "}:12092\n"

file = """Profiles:
    ComposerOrdererGenesis:
        Orderer:
            <<: *OrdererDefaults
            Organizations:
                - *OrdererOrg
        Consortiums:
            ComposerConsortium:
                Organizations:
                    - *Org1
    ComposerChannel:
        Consortium: ComposerConsortium
        Application:
            <<: *ApplicationDefaults
            Organizations:
                - *Org1
Organizations:
    - &OrdererOrg
        Name: OrdererOrg
        ID: OrdererMSP
        MSPDir: crypto-config/ordererOrganizations/example.com/msp
        AdminPrincipal: Role.MEMBER
    - &Org1
        Name: Org1
        ID: Org1MSP
        MSPDir: crypto-config/peerOrganizations/org1.example.com/msp
        AdminPrincipal: Role.MEMBER
        AnchorPeers:
            - Host: peer0.org1.example.com
              Port: 7051
""" + anchorPeers + """
Orderer: &OrdererDefaults
    OrdererType: kafka
    Addresses:
        - {IP-HOST-1}:7050
""" + orderers + """
    BatchTimeout: 2s
    BatchSize:
        MaxMessageCount: 10
        AbsoluteMaxBytes: 98 MB
        PreferredMaxBytes: 512 KB
    Kafka:
        Brokers:
            - {IP-HOST-1}:9092
            - {IP-HOST-1}:10092
            - {IP-HOST-1}:11092
            - {IP-HOST-1}:12092
""" + kafka + """
    Organizations:

Application: &ApplicationDefaults
    Organizations:
Capabilities:
    Global: &ChannelCapabilities
        V1_1: true
    Orderer: &OrdererCapabilities
        V1_1: true
    Application: &ApplicationCapabilities
        V1_1: true"""

text_file = open("composer/configtx.yaml", "w")
text_file.write(file)
text_file.close()