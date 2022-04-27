#### login to ECR
https://docs.aws.amazon.com/ko_kr/AmazonECR/latest/userguide/getting-started-cli.html
```
aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {aws_account_id}.dkr.ecr.{region}.amazonaws.com
```


# ECR 푸시 방법
1. ECR repository 생성
2. console에 push script있음.
3. AmazonEC2ContainerRegistryFullAccess 권한 필요(https://stackoverflow.com/questions/70452836/docker-push-to-aws-ecr-hangs-immediately-and-times-out)