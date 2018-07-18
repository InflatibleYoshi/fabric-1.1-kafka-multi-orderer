cd ~
sudo apt update && sudo apt upgrade -y
sudo apt install git make gcc g++ libltdl-dev curl python pkg-config nfs-common -y
curl -fsSL test.docker.com | sh
sudo usermod -aG docker $USER
exec sudo su -l $USER
cd multi-machine-HLF11