# Internal Developer Platform (IDP)

A self-service platform layer that gives product teams a paved road to ship containerized services with reliability, security, observability and cost controls built in, so they do not reinvent infrastructure per team. Opinionated Terraform golden-path modules, a self-service scaffolding CLI, and baked-in observability.

Maintained by nrobertio. A generic, public reference for platform-engineering work: shared platform capabilities, self-service tooling, and production readiness across a fleet of services.

## What this demonstrates

- Golden-path modules: an opinionated service-baseline Terraform module (ECS Fargate service, ALB wiring, autoscaling, least-privilege IAM, logs and alarms) so every service is production-ready by default.
- Self-service tooling: a Python CLI that scaffolds a new service (Terraform + Dockerfile + CI) from a template, so a team ships in minutes without deep infra knowledge.
- Observability by default: a reusable module that ships a CloudWatch dashboard and alarms with every service.
- Production readiness baked in: health checks, autoscaling, structured logging, alarms, and least-privilege roles are defaults, not add-ons.

## Layout

```
modules/service-baseline/   opinionated golden-path service (ECS Fargate + ALB + autoscale + IAM + logs)
modules/observability/      CloudWatch dashboard + alarms module
platform-cli/               Python CLI that scaffolds a ready-to-apply service
docs/PROJECT.md             why, how, benefits, interview notes
```

## Usage

```
python platform-cli/idp.py new-service payments
cd environments/dev && terraform init && terraform apply
```

## License

MIT. See LICENSE.
