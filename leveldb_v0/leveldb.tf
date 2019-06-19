provider "aws" {
  profile    = "${var.profile}"  
  region     = "${var.region}"
}

resource "aws_instance" "single" {
  ami = "ami-0abcc115edb9a5bb2"
  instance_type = "t2.xlarge"
  key_name = "${var.ami_key_pair_name}"
  security_groups = ["${var.security_group}"]

provisioner "file" {
    connection {
      type     = "ssh"
      user     = "ubuntu"
      private_key = "${file(var.private_key_path)}"
    }
    source      = "scripts/select_single_txn.py"
    destination = "/tmp/select_single_txn.py"
  }

provisioner "file" {
    connection {
      type     = "ssh"
      user     = "ubuntu"
      private_key = "${file(var.private_key_path)}"
    }
    source      = "scripts/get_txn_chain.py"
    destination = "/tmp/get_txn_chain.py"
  }

provisioner "file" {
    connection {
      type     = "ssh"
      user     = "ubuntu"
      private_key = "${file(var.private_key_path)}"
    }
    source      = "scripts/leveldb_v0_data_init.py"
    destination = "/tmp/leveldb_v0_data_init.py"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo mkdir -p /DATA/leveldb/onDiskDB ;
              sudo apt-get update ;
              sudo apt-get install -y libsnappy-dev ;
              sudo go get github.com/kanosaki/ldbsh ;
              sudo pip install plyvel ;
              cd /DATA/leveldb && wget https://github.com/google/leveldb/archive/1.22.tar.gz && tar xvf 1.22.tar.gz && rm -rf 1.22.tar.gz ;
              sleep 2m ;
              sudo python /tmp/leveldb_v0_data_init.py > /tmp/poc_bdd_leveldb_v0.log 2>&1 ; 
              EOF
  tags {
    Name = "poc_bdd_leveldb_v0_10000TX"
  }
}

