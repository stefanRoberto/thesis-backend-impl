resource "kubernetes_manifest" "issuer_le_http_thesis_api" {
  provider = kubernetes

  manifest = {
    apiVersion = "cert-manager.io/v1"
    kind       = "Issuer"

    metadata = {
      name      = "le-http-thesis-api"
      namespace = local.kubernetes_namespace
    }

    spec = {
      acme = {
        email  = local.acme_email
        server = var.ACME_SERVER

        privateKeySecretRef = {
          name = "thesis-api-issuer-account-key"
        }

        solvers = [
          {
            http01 = {
              ingress = {
                class = "traefik"
              }
            }
          }
        ]
      }
    }
  }
}

resource "kubernetes_ingress_v1" "traefik_thesis_api" {
  metadata {
    name      = "fastapi-ingress"
    namespace = local.kubernetes_namespace
    annotations = {
      "kubernetes.io/ingress.class"                      = "traefik"
      "traefik.ingress.kubernetes.io/ssl-redirect"       = "true"
      "traefik.ingress.kubernetes.io/redirect-permanent" = "true"
      "cert-manager.io/issuer"                           = kubernetes_manifest.issuer_le_http_thesis_api.manifest.metadata.name
    }
  }

  spec {
    tls {
      hosts       = [local.domain_name]
      secret_name = "tls-thesis-api-ingress-http"
    }

    rule {
      host = local.domain_name
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.fastapi.metadata.0.name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }

  depends_on = [kubernetes_manifest.issuer_le_http_thesis_api]
}