locals {
  vpc_name = "cluster-vpc"
  vpc_cidr = "10.0.0.0/16"
  vpc_azs  = slice(data.aws_availability_zones.available.names, 0, 3)

  eks_cluster_name     = "thesis-eks-cluster"
  kubernetes_namespace = "thesis"

  hosted_zone_name = "sroberto.site"
}