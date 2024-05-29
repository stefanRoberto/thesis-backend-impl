resource "helm_release" "mysql" {
  name       = "mysql"
  namespace  = kubernetes_namespace.thesis_namespace.metadata.0.name
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "mysql"
  version    = "10.1.1"

  set_sensitive {
    name  = "auth.username"
    value = var.DB_USERNAME
  }

  set_sensitive {
    name  = "auth.password"
    value = var.DB_PASSWORD
  }

  set_sensitive {
    name  = "auth.database"
    value = var.DB_NAME
  }

  set {
    name  = "primary.persistence.size"
    value = "10Gi"
  }

  depends_on = [module.eks, aws_iam_policy.ebs]
}

resource "helm_release" "traefik" {
  name             = "traefik"
  repository       = "https://helm.traefik.io/traefik"
  chart            = "traefik"
  namespace        = "traefik"
  create_namespace = true
  version          = "23.0.1"

  depends_on = [module.eks]
}

resource "helm_release" "cert_manager" {
  name             = "cert-manager"
  repository       = "https://charts.jetstack.io"
  chart            = "cert-manager"
  namespace        = "cert-manager"
  create_namespace = true
  version          = "1.14.5"

  set {
    name  = "installCRDs"
    value = "true"
  }

  depends_on = [module.eks]
}