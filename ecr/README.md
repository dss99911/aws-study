#### login to ECR
https://docs.aws.amazon.com/ko_kr/AmazonECR/latest/userguide/getting-started-cli.html
```
aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {aws_account_id}.dkr.ecr.{region}.amazonaws.com
```


# ECR 푸시 방법
1. ECR repository 생성
2. console에 push script있음.
3. AmazonEC2ContainerRegistryFullAccess 권한 필요(https://stackoverflow.com/questions/70452836/docker-push-to-aws-ecr-hangs-immediately-and-times-out)
```shell
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchGetImage",
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeImages",
        "ecr:DescribeRepositories",
        "ecr:GetDownloadUrlForLayer",
        "ecr:InitiateLayerUpload",
        "ecr:ListImages",
        "ecr:PutImage",
        "ecr:UploadLayerPart"
      ],
      "Resource": ["arn:aws:ecr:ap-south-1:123455555:repository/some-image"]
    },
    {
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    }
  ]
}
```

# untagged 자동 삭제
- Lifecycle Policy 라는 걸 설정 하면, untagged 자동 삭제 가능
- https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html
