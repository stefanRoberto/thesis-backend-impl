data "kubernetes_service" "traefik" {
  metadata {
    name      = "traefik"
    namespace = "traefik"
  }

  depends_on = [helm_release.traefik]
}

data "aws_elb_hosted_zone_id" "elb_zone_id" {}

resource "aws_route53_record" "eks_ingress_load_balancer" {
  zone_id = data.aws_route53_zone.hosted_zone.id
  name    = local.hosted_zone_name
  type    = "A"

  alias {
    name                   = data.kubernetes_service.traefik.status.0.load_balancer.0.ingress.0.hostname
    zone_id                = data.aws_elb_hosted_zone_id.elb_zone_id.id
    evaluate_target_health = true
  }
}