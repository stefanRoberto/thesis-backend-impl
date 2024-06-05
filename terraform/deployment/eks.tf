module "eks" {
  source       = "terraform-aws-modules/eks/aws"
  version      = "~> 20.8"
  cluster_name = local.eks_cluster_name

  cluster_version                          = "1.29"
  cluster_endpoint_public_access           = true
  enable_cluster_creator_admin_permissions = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }

    kube-proxy = {
      most_recent = true
    }

    vpc-cni = {
      most_recent = true

      configuration_values = jsonencode({
        enableNetworkPolicy : "true",
      })
    }

    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  vpc_id = module.vpc.vpc_id

  subnet_ids = module.vpc.private_subnets
  eks_managed_node_group_defaults = {
    ami_type       = "AL2_x86_64"
    instance_types = ["t3.medium"]
  }

  eks_managed_node_groups = {
    thesis-eks-cluster-wg = {
      min_size     = 1
      max_size     = 2
      desired_size = 1

      instance_types = ["t3.medium"]
      capacity_type  = "SPOT"

      iam_role_additional_policies = {
        EbsEksPolicy                       = aws_iam_policy.ebs.arn
        EcrEksPolicy                       = aws_iam_policy.ecr.arn
        AmazonEC2ContainerRegistryReadOnly = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
        Route53EksPolicy                   = aws_iam_policy.route53.arn
      }
    }
  }
}

resource "aws_iam_policy" "ebs" {
  name        = "terraform_cli_ebs_eks_policy"
  description = "Policy for managing EBS volumes within EKS cluster"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EbsEksStatement0"
        Effect = "Allow"
        Action = [
          "ec2:CreateVolume",
          "ec2:DeleteVolume",
          "ec2:DetachVolume",
          "ec2:AttachVolume",
          "ec2:DescribeInstances",
          "ec2:CreateTags",
          "ec2:DeleteTags",
          "ec2:DescribeTags",
          "ec2:DescribeVolumes"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "ecr" {
  name        = "terraform_cli_ecr_eks_policy"
  description = "Policy for using ECR images within EKS cluster"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EcrEksStatement0"
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "route53" {
  name        = "terraform_cli_route53_eks_policy"
  description = "Policy for accessing Route53 records within EKS cluster"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "route53:GetChange"
        ]
        Resource = "arn:aws:route53:::change/*"
      },
      {
        Effect = "Allow"
        Action = [
          "route53:ChangeResourceRecordSets",
          "route53:ListResourceRecordSets"
        ]
        Resource = "arn:aws:route53:::hostedzone/${data.aws_route53_zone.hosted_zone.id}"
      }
    ]
  })
}

data "aws_route53_zone" "hosted_zone" {
  name         = local.hosted_zone_name
  private_zone = false
}