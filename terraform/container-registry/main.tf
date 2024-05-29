terraform {
  required_version = ">= 1.8.0"

  backend "s3" {
    bucket         = "thesis-api-terraform-state"
    key            = "tf-infra-container-registry/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "thesis-api-terraform-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40"
    }
  }
}