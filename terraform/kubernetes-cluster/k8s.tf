resource "kubernetes_namespace" "thesis_namespace" {
  metadata {
    name = local.kubernetes_namespace
  }
}