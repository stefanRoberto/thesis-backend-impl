resource "aws_ecr_repository" "api_ecr_repository" {
  name                 = local.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  force_delete = true

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "api_ecr_repository_lifecycle_policy" {
  repository = aws_ecr_repository.api_ecr_repository.name

  policy = <<EOF
  {
    "rules": [
      {
        "rulePriority": 1,
        "description": "Expire untagged images older than 14 days",
        "selection": {
          "tagStatus": "untagged",
          "countType": "sinceImagePushed",
          "countUnit": "days",
          "countNumber": 14
        },
        "action": {
          "type": "expire"
        }
      },
      {
        "rulePriority": 2,
        "description": "Keep last 3 images",
        "selection": {
            "tagStatus": "tagged",
            "tagPrefixList": ["prod"],
            "countType": "imageCountMoreThan",
            "countNumber": 3
        },
        "action": {
            "type": "expire"
        }
      }
    ]
  }
  EOF
}