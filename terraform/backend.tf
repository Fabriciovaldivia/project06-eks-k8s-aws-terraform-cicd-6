terraform {
  backend "s3" {
    bucket  = "proyecto06-terraform-state-eks"
    key     = "eks/terraform.tfstate"
    region  = "us-east-1"
    # use_lockfile = true   # prefer this over dynamodb_table for state locking
    encrypt = true
  }
}
