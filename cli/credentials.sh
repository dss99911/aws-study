# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

# 1. make user on IAM
# 2. give permission for the user


#Make default credentials.
# keys, regison, default-format(json)
aws configure

#Make different credentials
aws configure --profile {profile-name}

aws {somemethod} --profile {profile-name}

#여러 명령어에 다른 profile을 사용하고 싶은 경우.
export AWS_PROFILE=user1

#use profile
aws some-service --profile hyun
#use region
aws some-service --region ap-south-1