# IDP self-service CLI.
# Scaffolds a new service from the golden-path template so a team can ship
# without writing infrastructure by hand. Generates a Terraform file that
# calls the service-baseline module plus the observability module.
import argparse
import os
import re

TEMPLATE = '''module "{name}" {{
  source             = "../../modules/service-baseline"
  name               = "{name}"
  image              = "{image}"
  container_port     = {port}
  cluster_arn        = var.cluster_arn
  subnet_ids         = var.private_subnet_ids
  security_group_ids = [var.service_sg_id]
  target_group_arn   = var.target_group_arn
}}

module "{name}_observability" {{
  source          = "../../modules/observability"
  name            = "{name}"
  alarm_topic_arn = var.alarm_topic_arn
}}
'''


def valid_name(name):
    if not re.match(r"^[a-z][a-z0-9-]{{1,30}}$", name):
        raise SystemExit("service name must be lowercase letters, digits and hyphens")
    return name


def new_service(name, image, port, out_dir):
    valid_name(name)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name + ".tf")
    with open(path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(name=name, image=image, port=port))
    print("Created " + path)
    print("Next: cd " + out_dir + " && terraform init && terraform apply")


def main():
    parser = argparse.ArgumentParser(description="IDP self-service scaffolder")
    sub = parser.add_subparsers(dest="cmd", required=True)
    ns = sub.add_parser("new-service", help="scaffold a new golden-path service")
    ns.add_argument("name")
    ns.add_argument("--image", default="public.ecr.aws/nginx/nginx:latest")
    ns.add_argument("--port", type=int, default=8080)
    ns.add_argument("--out-dir", default="environments/dev")
    args = parser.parse_args()
    if args.cmd == "new-service":
        new_service(args.name, args.image, args.port, args.out_dir)


if __name__ == "__main__":
    main()
