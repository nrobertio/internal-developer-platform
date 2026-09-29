output "service_name" { value = aws_ecs_service.svc.name }
output "task_role_arn" { value = aws_iam_role.task.arn }
output "log_group" { value = aws_cloudwatch_log_group.svc.name }
