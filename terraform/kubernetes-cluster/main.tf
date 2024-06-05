terraform {
  required_version = ">= 1.8.0"

  backend "s3" {
    bucket         = "thesis-api-terraform-state"
    key            = "tf-infra-kubernetes-cluster/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "thesis-api-terraform-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.29.0"
    }

    helm = {
      source  = "hashicorp/helm"
      version = "2.13.1"
    }
  }
}