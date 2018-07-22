import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

OrdererSANS = ""
PeerSANS  = ""
arg1 -= 1
for i in range(arg1):
    OrdererSANS += '      - Hostname: orderer' + str( (i+1)) + '\n'
    OrdererSANS += '        SANS:\n'
    OrdererSANS += '          - {IP-HOST-' + str( (i+2)) + '}\n'

for i in range(arg1):
    PeerSANS += '          - {IP-HOST-' + str( (i+2)) + '}\n'

file = """OrdererOrgs:
  - Name: Orderer
    Domain: example.com
    Specs:
      - Hostname: orderer0
        SANS:
          - {IP-HOST-1}
""" + OrdererSANS + """
PeerOrgs:
  - Name: Org1
    Domain: org1.example.com
    EnableNodeOUs: true
    Specs:
      - Hostname: peer
        SANS:
          - {IP-HOST-1}
""" + PeerSANS + """
    Template:
      Count: """ + str( (arg1 + 1) * 2 ) +  """
    Users:
      Count: 0 """

text_file = open("composer/crypto-config.yaml", "w")
text_file.write(file)
text_file.close()