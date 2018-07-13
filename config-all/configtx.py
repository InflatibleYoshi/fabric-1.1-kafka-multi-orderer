import string
from subprocess import call
import sys, getopt

def main(arg1, *argv):
    anchorPeers = ""
    orderers  = ""
    arg1 -= 1
    for i in range(arg1):
        anchorPeers += "         - peer" + (i+1) * 2 + ".org1.example.com\n"
        anchorPeers += "         - Port: 9051\n"
    call("sed -i -e 's/{Anchor Peers}/"+ anchorPeers + "/g' ../composer/configtx.yaml")

    for i in range(arg1):
        orderers += "      - {IP-HOST-" + (i+1)+ "}:7050\n"    
    call("sed -i -e 's/{Orderers}/"+ orderers + "/g' ../composer/configtx.yaml")
