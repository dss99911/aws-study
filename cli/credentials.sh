# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

# 1. make user on IAM
# 2. give permission for the user


#Make default credentials.
# keys, regison, default-format(json)
aws configure

#Make different credentials
aws configure --profile {profile-name}

aws {somemethod} --profile {profile-name}


#use profile
aws some-service --profile hyun
#use region
aws some-service --region ap-south-1