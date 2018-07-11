cd "$(dirname "$0")"

HOST1="10.0.0.113"
HOST2="10.0.0.92"

sed -i -e "s/{IP-HOST-1}/$HOST1/g" configtx.yaml
sed -i -e "s/{IP-HOST-2}/$HOST1/g" configtx.yaml
sed -i -e "s/{IP-HOST-1}/$HOST1/g" crypto-config.yaml
sed -i -e "s/{IP-HOST-2}/$HOST2/g" crypto-config.yaml
sed -i -e "s/{IP-HOST-1}/$HOST1/g" ../createPeerAdminCard.sh
sed -i -e "s/{IP-HOST-2}/$HOST2/g" ../createPeerAdminCard.sh

cryptogen generate --config=./crypto-config.yaml
export FABRIC_CFG_PATH=$PWD
configtxgen -profile ComposerOrdererGenesis -outputBlock ./composer-genesis.block
configtxgen -profile ComposerChannel -outputCreateChannelTx ./composer-channel.tx -channelID composerchannel

ORG1KEY="$(ls crypto-config/peerOrganizations/org1.example.com/ca/ | grep 'sk$')"

sed -i -e "s/{ORG1-CA-KEY}/$ORG1KEY/g" docker-compose.yml

