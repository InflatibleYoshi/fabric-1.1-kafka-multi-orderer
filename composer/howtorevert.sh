cd "$(dirname "$0")"

HOST1="10.0.0.113"
HOST2="10.0.0.92"

sed -i -e "s/$HOST1/{IP-HOST-1}/g" configtx.yaml
sed -i -e "s/$HOST2/{IP-HOST-2}/g" configtx.yaml
sed -i -e "s/$HOST1/{IP-HOST-1}/g" crypto-config.yaml
sed -i -e "s/$HOST2/{IP-HOST-2}/g" crypto-config.yaml
sed -i -e "s/$HOST1/{IP-HOST-1}/g" docker-compose.yml
sed -i -e "s/$HOST1/{IP-HOST-1}/g" docker-compose-peer2.yml
sed -i -e "s/$HOST1/{IP-HOST-1}/g" ../createPeerAdminCard.sh
sed -i -e "s/$HOST2/{IP-HOST-2}/g" ../createPeerAdminCard.sh

ORG1KEY="$(ls crypto-config/peerOrganizations/org1.example.com/ca/ | grep 'sk$')"

sed -i -e "s/$ORG1KEY/{ORG1-CA-KEY}/g" docker-compose.yml

rm -rf composer* crypto-config
