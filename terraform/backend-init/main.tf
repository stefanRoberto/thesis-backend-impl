terraform {
  required_version = ">= 1.8.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40"
    }
  }
}

module "tf-state" {
  source      = "./modules/tf-state"
  bucket_name = "thesis-api-terraform-state"
  table_name  = "thesis-api-terraform-locks"
}
