# Terraform install

```
terraform init
terraform plan
terraform apply
```
### On first machine → 192.168.1.5
```
cd fabric-1.1-kafka-multi-orderer/ 
cd composer
chmod +x howtobuild.sh
./howtobuild.sh
cd ..
./startFabric.sh
```

### On all other machines 192.168.1.6…
```
write “192.168.1.5 orderer0 orderer0.example.com” >> /etc/hosts
cd fabric-1.1-kafka-multi-orderer/
chmod +x startFabric-peer(n).sh
./startFabric-Peer(n).sh
```
### On all machines
```
chmod +x createPeerAdminCard.sh
./createPeerAdminCard.sh
composer-playground
```