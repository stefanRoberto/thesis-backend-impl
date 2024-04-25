locals {
  vpc_name            = "cluster-vpc"
  vpc_cidr            = "10.10.0.0/16"
  vpc_azs             = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  vpc_private_subnets = ["10.10.1.0/24", "10.10.2.0/24", "10.10.3.0/24"]
  vpc_public_subnets  = ["10.10.101.0/24", "10.10.102.0/24", "10.10.103.0/24"]
  vpc_intra_subnets   = ["10.10.11.0/24", "10.10.12.0/24", "10.10.13.0/24"]

  eks_cluster_name = "thesis-eks-cluster"

}