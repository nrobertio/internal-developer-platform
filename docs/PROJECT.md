# Project Writeup: Internal Developer Platform

Why this exists, how it was built, why each choice, benefits, and interview talking points. Maps to platform-engineering roles that ask for shared platform capabilities, self-service tooling, and production readiness.

## 1. The problem it solves

In a company with many teams, each team reinventing infrastructure produces inconsistency, drift and risk: one team forgets autoscaling, another logs nothing, a third runs over-privileged. Platform engineering fixes this with a paved road (golden path): an opinionated, self-service way to ship that has reliability, security, observability and cost controls built in. Teams move faster and the fleet stays consistent.

## 2. How it was built

- A service-baseline Terraform module: an ECS Fargate service with ALB wiring, CPU autoscaling, least-privilege task and execution roles, and a CloudWatch log group. Using it makes a service production-ready by default.
- An observability module: a CloudWatch dashboard and a CPU alarm shipped with every service.
- A self-service CLI (Python): "idp new-service" generates a ready-to-apply Terraform file that calls the modules, so a team ships without hand-writing infrastructure.

## 3. Why each choice

- Golden-path modules over a wiki of best practices: a module enforces the good defaults; documentation only suggests them. Autoscaling, logging and least privilege are not optional here.
- ECS Fargate for the baseline: no servers to patch, simple mental model, cheaper and lower-ops than EKS for typical services. The pattern generalizes to EKS where teams need it.
- Self-service CLI: reduces the platform team from a ticket queue to a paved road. A team runs one command instead of filing a request and waiting.
- Observability shipped with the service, not bolted on later: you cannot operate what you cannot see, so every service gets a dashboard and an alarm from day one.
- ALB target-group health checks rather than container-level checks: the load balancer is the right place to decide if a task is healthy and should receive traffic.

## 4. Benefits

- Developer velocity: a new service is one command plus an apply, not a bespoke infra project.
- Consistency and reduced drift: every service has the same production-ready shape.
- Security by default: least-privilege roles and private networking are baked in.
- Operability: logs, dashboards and alarms exist from the first deploy.
- Cost control: right-sized defaults and autoscaling instead of always-on over-provisioning.

## 5. Interview talking points

- What a golden path is and why it beats documentation: it enforces defaults instead of suggesting them.
- Platform team as a product team: the internal customers are engineers; the CLI and modules are the product; success is adoption and developer velocity.
- Why observability ships with the service: operability is a property of the platform, not an afterthought per team.
- Trade-offs of an opinionated platform: less flexibility per team, in exchange for consistency, security and speed; provide escape hatches for genuine exceptions.
- What to add next: a service catalog (Backstage), progressive delivery, policy-as-code (OPA/Kyverno) to enforce standards, and golden-path variants for EKS and edge (k3s).

## 6. How to run it

```
python platform-cli/idp.py new-service payments
cd environments/dev
terraform init
terraform apply
```

The modules assume you provide the shared inputs (ECS cluster, subnets, security group, ALB target group, alarm SNS topic) from your own base infrastructure.