module "vpc" {
  source = "./modules/vpc"

  name = "vpc-proyecto-05"
  cidr = var.vpc_cidr
}

module "eks" {
  source = "./modules/eks"

  cluster_name   = var.cluster_name
  vpc_id         = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets
}
