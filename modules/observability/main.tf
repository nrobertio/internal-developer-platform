# Ships a dashboard and alarms with every service, so observability is default.
resource "aws_cloudwatch_dashboard" "svc" {
  dashboard_name = "${var.name}-service"
  dashboard_body = jsonencode({
    widgets = [{
      type   = "metric"
      width  = 12
      height = 6
      properties = {
        title  = "${var.name} CPU and Memory"
        region = "eu-central-1"
        metrics = [
          ["AWS/ECS", "CPUUtilization", "ServiceName", var.name],
          ["AWS/ECS", "MemoryUtilization", "ServiceName", var.name]
        ]
      }
    }]
  })
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.name}-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 60
  statistic           = "Average"
  threshold           = 85
  dimensions          = { ServiceName = var.name }
  alarm_actions       = [var.alarm_topic_arn]
}
