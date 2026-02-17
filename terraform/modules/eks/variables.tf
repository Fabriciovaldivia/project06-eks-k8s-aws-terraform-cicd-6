variable "cluster_name" {
  description = "Nombre del cluster EKS"
  type        = string
}

variable "vpc_id" {
  description = "ID de la VPC"
  type        = string
}

variable "private_subnets" {
  description = "Lista de subnets privadas para los nodos"
  type        = list(string)
}

variable "node_role_arn" {
  description = "ARN del rol IAM para los nodos (creado en el modulo security)"
  type        = string
}

variable "cluster_role_arn" {
  description = "ARN del rol IAM para el control plane de EKS"
  type        = string
}