provider "aws" {
  profile    = "${var.profile}"  
  region     = "${var.region}"
}

resource "aws_instance" "single" {
  ami = "ami-0e2f8b6407c122aff"
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
    source      = "scripts/mongo_v0_data_init.py"
    destination = "/tmp/mongo_v0_data_init.py"
  }




  user_data = <<-EOF
              #!/bin/bash
              sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 68818C72E52529D4 ;
              sudo echo "deb http://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list ;
              sudo mkdir -p /DATA/mongodb ;
              sudo ln -s /DATA/mongodb /var/lib/mongodb ;
              sudo apt-get update ;
              sudo apt-get install -y mongodb-org python2.7 python-pip ;
              sudo chown -R mongodb:mongodb /DATA/mongodb ;
              sudo chown mongodb:mongodb /var/lib/mongodb ;
              sudo systemctl start mongod ;
              sudo systemctl enable mongod ;
              sudo pip install pymongo 
              EOF

  tags {
    Name = "poc_bdd_mongo_v0"
  }
}

