# dev environment

Generated services land here as `<name>.tf`, each calling the golden-path modules. Wire the shared inputs (cluster_arn, private_subnet_ids, service_sg_id, target_group_arn, alarm_topic_arn) in your own variables, then `terraform init && terraform apply`.
