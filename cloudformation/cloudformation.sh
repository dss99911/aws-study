# create
aws cloudformation create-stack --stack-name devcluster --template-body file://dev.yaml

# delete
aws cloudformation delete-stack --stack-name devcluster
