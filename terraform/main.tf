module "vpc" {
  source = "./modules/vpc"

  name = "vpc-proyecto06"
  cidr = var.vpc_cidr
}

module "security" {
  source = "./modules/security"

  cluster_name = var.cluster_name
}

module "eks" {
  source = "./modules/eks"

  cluster_name   = var.cluster_name
  vpc_id         = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets
  node_role_arn   = module.security.node_role_arn
  cluster_role_arn = module.security.cluster_role_arn
}
