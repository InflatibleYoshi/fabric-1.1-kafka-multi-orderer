# Hyperledger Fabric 1.1 TLS + KAFKA + MULTI MACHINE + MULTI ORDERER setup

### This is no longer a work in progress but I do not consider this build 100% complete unless it is subject to some testing.

```
git clone https://github.com/InflatibleYoshi/fabric-1.1-kafka-multi-orderer
cd fabric-1.1-kafka-multi-orderer
./installPrerequisites.sh
./installPrerequisites2.sh
python start.py {# of peers}
cd composer
```
### Change the IP addresses in howtobuild.sh and set them to the ip addresses of each host
```
chmod +x howtobuild.sh
./howtobuild.sh
cd ..
chmod +x startFabric.sh
```
### scp the directory to all the peers.
```
# write “'HOST1-IP' orderer0 orderer0.example.com” to /etc/hosts
cd fabric-1.1-kafka-multi-orderer/
chmod +x startFabric-Peer(n).sh
./startFabric-Peer(n).sh
chmod +x createPeerAdminCard.sh
./createPeerAdminCard.sh
composer-playground
```