import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

OrdererSANS = ""
PeerSANS  = ""
for i in range(arg1):
    OrdererSANS += '      - Hostname: orderer' + str(i) + '\n'
    OrdererSANS += '        SANS:\n'
    OrdererSANS += '          - {IP-HOST-' + str( (i+1)) + '}\n'

for i in range(arg1):
    PeerSANS += '          - {IP-HOST-' + str( (i+1)) + '}\n'

file = """OrdererOrgs:
  - Name: Orderer
    Domain: example.com
    Specs:
""" + OrdererSANS + """
PeerOrgs:
  - Name: Org1
    Domain: org1.example.com
    EnableNodeOUs: true
    Specs:
      - Hostname: peer
        SANS:
""" + PeerSANS + """
    Template:
      Count: """ + str( (arg1) * 2 ) +  """
    Users:
      Count: 0 """

text_file = open("composer/crypto-config.yaml", "w")
text_file.write(file)
text_file.close()