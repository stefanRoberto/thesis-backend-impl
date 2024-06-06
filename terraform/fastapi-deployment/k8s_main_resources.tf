data "aws_ecr_repository" "thesis_api" {
  name = local.ecr_repository_name
}

data "aws_ecr_image" "fastapi_latest" {
  repository_name = local.ecr_repository_name
  image_tag       = var.IMAGE_TAG
}

resource "kubernetes_secret" "mysql_credentials" {
  metadata {
    name      = "mysql-credentials"
    namespace = local.kubernetes_namespace
  }

  type = "Opaque"

  data = {
    DB_USERNAME = var.DB_USERNAME
    DB_PASSWORD = var.DB_PASSWORD
    DB_NAME     = var.DB_NAME
  }
}

resource "kubernetes_deployment" "fastapi" {
  metadata {
    name      = "fastapi-deployment"
    namespace = local.kubernetes_namespace
    labels = {
      app = "fastapi"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "fastapi"
      }
    }

    template {
      metadata {
        labels = {
          app = "fastapi"
        }
      }

      spec {
        container {
          name              = "fastapi"
          image             = data.aws_ecr_image.fastapi_latest.image_uri
          image_pull_policy = "Always"

          env {
            name = "DB_USERNAME"
            value_from {
              secret_key_ref {
                name = "mysql-credentials"
                key  = "DB_USERNAME"
              }
            }
          }

          env {
            name = "DB_PASSWORD"
            value_from {
              secret_key_ref {
                name = "mysql-credentials"
                key  = "DB_PASSWORD"
              }
            }
          }

          env {
            name = "DB_NAME"
            value_from {
              secret_key_ref {
                name = "mysql-credentials"
                key  = "DB_NAME"
              }
            }
          }

          env {
            name  = "DB_HOST"
            value = "mysql"
          }

          port {
            container_port = 80
          }
        }
      }
    }
  }

  depends_on = [kubernetes_secret.mysql_credentials]

  timeouts {
    create = "2m"
    update = "2m"
    delete = "2m"
  }
}

resource "kubernetes_service" "fastapi" {
  metadata {
    name      = "fastapi-service"
    namespace = local.kubernetes_namespace
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "fastapi"
    }

    port {
      protocol    = "TCP"
      port        = 80
      target_port = 80
    }
  }

  depends_on = [kubernetes_deployment.fastapi]
}