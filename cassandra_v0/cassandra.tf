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
    source      = "scripts/cassandra_v0.cql"
    destination = "/tmp/cassandra_v0.cql"
  }

  provisioner "file" {
    connection {
      type     = "ssh"
      user     = "ubuntu"
      private_key = "${file(var.private_key_path)}"
    }
    source      = "scripts/cassandra_v0_data_init.py"
    destination = "/tmp/cassandra_v0_data_init.py"
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
              echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list ;
              sudo apt install -y curl python2.7 python-pip ;
              sudo ln -s /usr/bin/python2.7 /usr/bin/python ;
              sudo pip install cassandra-driver ;
              curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add - ;
              sudo apt update ;
              sudo mkdir -p /DATA/cassandra/data /DATA/cassandra/commitlog /DATA/cassandra/saved_caches ;
              sudo ln -s /DATA/cassandra /var/lib/cassandra ;
              sudo apt install -y cassandra ;
              sudo chown -R cassandra:cassandra /DATA/cassandra ;
              sudo chown cassandra:cassandra /var/lib/cassandra ;
              sudo sed  -i 's/#-Xmx4G/-Xmx8G/g' /etc/cassandra/jvm.options ;
              sudo sed  -i 's/#-Xms4G/-Xms4G/g' /etc/cassandra/jvm.options ;
              sudo systemctl enable cassandra ;
              sudo systemctl start cassandra ;
              sleep 2m;
              sudo cqlsh < /tmp/cassandra_v0.cql > /tmp/poc_bdd_cassandra_v0.log 2>&1 ;
              sudo python /tmp/cassandra_v0_data_init.py >> /tmp/poc_bdd_cassandra_v0.log 2>&1 ; 
              EOF

  tags {
    Name = "poc_bdd_cassandra_v0"
  }
}

