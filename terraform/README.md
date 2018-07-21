# Terraform install

Before you begin the install, make sure you have terraform installed on your computer and your AWS certificates are in the default location according to your OS: (Linux: ~/.aws/credentials). They should be in this form:
```
[default]
aws_access_key_id = {YOUR ID}
aws_secret_access_key = {YOUR KEY}
```

Edit the number of peers in main.tf to your desire and ensure that you are using the correct ssh key.

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