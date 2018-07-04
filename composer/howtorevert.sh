cd "$(dirname "$0")"

HOST1="192.168.1.222"
HOST2="192.168.1.224"

sed -i -e "s/$HOST1/{IP-HOST-1}/g" configtx.yaml
sed -i -e "s/$HOST1/{IP-HOST-1}/g" docker-compose.yml
sed -i -e "s/$HOST1/{IP-HOST-1}/g" docker-compose-peer2.yml

sed -i -e "s/$HOST1/{IP-HOST-1}/g" ../createPeerAdminCard.sh
sed -i -e "s/$HOST2/{IP-HOST-2}/g" ../createPeerAdminCard.sh

ORG1KEY="$(ls crypto-config/peerOrganizations/org1.example.com/ca/ | grep 'sk$')"
ORG2KEY="$(ls crypto-config/peerOrganizations/org2.example.com/ca/ | grep 'sk$')"

sed -i -e "s/$ORG1KEY/{ORG1-CA-KEY}/g" docker-compose.yml
sed -i -e "s/$ORG2KEY/{ORG1-CA-KEY}/g" docker-compose-peer2.yml

rm -rf composer* crypto-config
