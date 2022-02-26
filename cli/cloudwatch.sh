# logs cli : https://docs.aws.amazon.com/cli/latest/reference/logs/index.html

# export log to s3.
# need permision of logs.CreateExportTask
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3ExportTasks.html
#   - need to change s3 bucket policy for logs service to access s3(refer step3)
aws logs create-export-task \
  --task-name 'test' \
  --log-group-name "/aws/lambda/test" \
  --log-stream-name-prefix '2021/09/12/[$LATEST]8cc82343d7d64d7d93040c4d44e47664' \
  --from 1441490400000 \
  --to 1741494000000 \
  --destination "hyun" \
  --destination-prefix "logs/test3" \
  --region ap-south-1

# just show logs. it has limit. and also shows the log by json format. so difficult to see the log
aws logs get-log-events \
  --log-group-name "/aws/lambda/test" \
  --log-stream-name '2021/09/12/[$LATEST]8cc82343d7d64d7d93040c4d44e47664' \
  --start-time 1441490400000 \
  --end-time 1641494000000 \
  --region ap-south-1