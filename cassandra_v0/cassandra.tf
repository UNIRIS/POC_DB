provider "aws" {
  profile    = "${var.profile}"  
  region     = "${var.region}"
}

resource "aws_instance" "single" {
  ami = "ami-0e2f8b6407c122aff"
  instance_type = "t2.xlarge"
  key_name = "${var.ami_key_pair_name}"
  security_groups = ["${var.security_group}"]

  user_data = <<-EOF
              #!/bin/bash
              echo "deb http://www.apache.org/dist/cassandra/debian 39x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
              sudo apt install curl
              curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
              sudo apt update
              sudo mkdir -p /DATA/cassandra/data /DATA/cassandra/commitlog /DATA/cassandra/saved_caches
              sudo ln -s /DATA/cassandra /var/lib/cassandra
              sudo apt install -y cassandra
              sudo chown -R cassandra:cassandra /DATA/cassandra
              sudo chown cassandra:cassandra /var/lib/cassandra
              sudo systemctl enable cassandra
              sudo systemctl start cassandra
              EOF

  tags {
    Name = "poc_bdd_cassandra_v0"
  }
}

