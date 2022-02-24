
# https://docs.aws.amazon.com/cli/latest/reference/sts/index.html#cli-aws-sts

# 현재 caller의 정보를 가져온다.
aws sts get-caller-identity
# {
#    "UserId": "AAAAAAAAAAA",
#    "Account": "123456789012",
#    "Arn": "arn:aws:iam::123456789012:user/DevAdmin"
#}