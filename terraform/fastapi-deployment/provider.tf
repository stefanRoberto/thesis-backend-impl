provider "aws" {
  region = "eu-central-1"
}

data "aws_eks_cluster" "thesis_eks_cluster" {
  name = local.eks_cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.thesis_eks_cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.thesis_eks_cluster.certificate_authority.0.data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.thesis_eks_cluster.name]
  }
}