name=$1
region=ap-south-1
account_id=111111
ecr_uri=${account_id}.dkr.ecr.${region}.amazonaws.com
slack_webhook_url=https://hooks.slack.com/services/123123123

set -e

aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $ecr_uri
aws ecr create-repository --repository-name $name --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE | true
docker build -f "$name/Dockerfile" -t $name .
docker tag "$name:latest" "$ecr_uri/$name:latest"
docker push "$ecr_uri/$name:latest"

#send slack message
curl -X POST -H 'Content-type: application/json' --data '{"text":"'$name' is updated"}' $slack_webhook_url