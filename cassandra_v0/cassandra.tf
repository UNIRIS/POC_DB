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
              echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list > /tmp/poc_bdd_cassandra_v0.log 2>&1 ;
              sudo pip install cassandra-driver >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add - ;
              sudo apt update >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo mkdir -p /DATA/cassandra/data /DATA/cassandra/commitlog /DATA/cassandra/saved_caches >> /tmp/poc_bdd_cassandra_v0.log 2>&1 ;
              sudo ln -s /DATA/cassandra /var/lib/cassandra >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo apt install -y cassandra >> /tmp/poc_bdd_cassandra_v0.log 2>&1 ;
              sudo chown -R cassandra:cassandra /DATA/cassandra >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo chown cassandra:cassandra /var/lib/cassandra >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo sed  -i 's/#-Xmx4G/-Xmx8G/g' /etc/cassandra/jvm.options >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo sed  -i 's/#-Xms4G/-Xms4G/g' /etc/cassandra/jvm.options >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo systemctl enable cassandra >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sudo systemctl start cassandra >> /tmp/poc_bdd_cassandra_v0.log 2>&1;
              sleep 2m ;
              sudo cqlsh < /tmp/cassandra_v0.cql >> /tmp/poc_bdd_cassandra_v0.log 2>&1 ;
              sudo python /tmp/cassandra_v0_data_init.py >> /tmp/poc_bdd_cassandra_v0.log 2>&1 ; 
              EOF

  tags {
    Name = "poc_bdd_cassandra_v0_10TX"
  }
}

