variable "profile" {
  description = "AWS credentials profile"
}

variable "region" {
  description = "Paris"
  default = "eu-west-3"
}

variable "ami_key_pair_name" {
  default = "abdelkarim"
}

variable "security_group" {
  default = "default_linux"
}

variable "private_key_path" {
  default = "/home/ba3aw/.ssh/id_rsa"
}