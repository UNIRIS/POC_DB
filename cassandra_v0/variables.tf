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
