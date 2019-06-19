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
    source      = "conf/aerospike.conf"
    destination = "/tmp/aerospike.conf"
  }
  provisioner "file" {
    connection {
      type     = "ssh"
      user     = "ubuntu"
      private_key = "${file(var.private_key_path)}"
    }
    source      = "scripts/aerospike_v0_data_init.py"
    destination = "/tmp/aerospike_v0_data_init.py"
  }

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


  user_data = <<-EOF
            #!/bin/bash
            sudo apt-get update
            sudo apt install -y python-dev libssl-dev zlib1g-dev;
            sudo pip install aerospike ;
            cd /tmp && wget -O aerospike.tgz 'https://www.aerospike.com/download/server/latest/artifact/ubuntu18' ;
            tar -xvf aerospike.tgz ;
            sleep 1m ;
            cd aerospike-server-community-4.5.3.3-ubuntu18.04 && ./asinstall
            mkdir -p /DATA/aerospike/data && chown -R aerospike:aerospike /DATA/aerospike ;
            sudo cp /tmp/aerospike.conf /etc/aerospike/aerospike.conf && sudo chown root:root /etc/aerospike/aerospike.conf && chmod 644 /etc/aerospike/aerospike.conf
            sudo systemctl enable aerospike ;
            sudo systemctl start aerospike ;
            sleep 2m ;
            sudo python /tmp/aerospike_v0_data_init.py > /tmp/poc_bdd_aerospike_v0.log 2>&1 ; 
            EOF

  tags {
    Name = "poc_bdd_aerospike_v0_10TX"
  }
}

