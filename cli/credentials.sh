# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

#Make default credentials.
# keys, regison, default-format(json)
aws configure

#Make different credentials
aws configure --profile {profile-name}

aws {somemethod} --profile {profile-name}