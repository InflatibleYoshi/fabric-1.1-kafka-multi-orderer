provider "aws" {
  region = "us-east-1"
}

variable "n" {
  default = 2
}

variable "public_key_path" {
  description = "Enter the path to the SSH Public Key to add to AWS."
  default     = "~/.ssh/id_rsa.pub"
}

resource "aws_key_pair" "auth" {
  key_name   = "default"
  public_key = "${file(var.public_key_path)}"
}

resource "aws_efs_file_system" "blockchain-data" {}

resource "aws_efs_mount_target" "multi-machine-HLF11" {
  ip_address      = "192.168.1.240"
  file_system_id  = "${aws_efs_file_system.blockchain-data.id}"
  subnet_id       = "${aws_subnet.fabric-subnet.id}"
  security_groups = ["${aws_security_group.allow_http.id}"]
  depends_on      = ["aws_efs_file_system.blockchain-data"]
}

resource "aws_instance" "fabric" {
  count                  = 1
  availability_zone      = "us-east-1a"
  private_ip             = "192.168.1.5"
  ami                    = "ami-69043c16"
  instance_type          = "t2.large"
  key_name               = "default"
  subnet_id              = "${aws_subnet.fabric-subnet.id}"
  vpc_security_group_ids = ["${aws_security_group.allow_http.id}"]

  provisioner "remote-exec" {
    inline = [
      "sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 192.168.1.240:/ /home/ubuntu/multi-machine-HLF11",
      "sudo git clone https://github.com/jean507/multi-machine-HLF11",
      "cd multi-machine-HLF11",
      "python start.py ${var.n} terraform",
      "cd composer",
      "./howtobuild.sh",
      "cd ..",
      "./startFabric.sh",
      "./createPeerAdminCard.sh",
      "composer-playground",
    ]

    connection {
      type = "ssh"
      user = "ubuntu"
    }
  }

  depends_on = ["aws_efs_mount_target.multi-machine-HLF11"]
}

resource "aws_instance" "fabric-peers" {
  count                  = "${var.n - 1}"
  availability_zone      = "us-east-1a"
  private_ip             = "192.168.1.${count.index + 6}"
  ami                    = "ami-69043c16"
  instance_type          = "t2.large"
  key_name               = "default"
  subnet_id              = "${aws_subnet.fabric-subnet.id}"
  vpc_security_group_ids = ["${aws_security_group.allow_http.id}"]

  provisioner "remote-exec" {
    inline = [
      "sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 192.168.1.240:/ /home/ubuntu/multi-machine-HLF11",
      "cd multi-machine-HLF11",
      "./startFabric-Peer${count.index + 2}.sh",
      "./createPeerAdminCard.sh",
      "composer-playground",
    ]

    connection {
      type = "ssh"
      user = "ubuntu"
    }
  }

  depends_on = ["aws_instance.fabric"]
}

resource "aws_vpc" "fabric-vpc" {
  cidr_block           = "192.168.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.fabric-vpc.id}"
}

resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.fabric-vpc.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.default.id}"
}

resource "aws_subnet" "fabric-subnet" {
  vpc_id                  = "${aws_vpc.fabric-vpc.id}"
  cidr_block              = "192.168.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
}

resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP traffic"
  vpc_id      = "${aws_vpc.fabric-vpc.id}"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["192.168.1.0/24"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8181
    to_port     = 8181
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
