set -e

export AWS_PROFILE=default
BUCKET=tb.es
CLUSTER_NAME=DS_CLUSTER


aws s3 cp data/bootstrap.sh s3://$BUCKET/emr/$CLUSTER_NAME/bootstrap.sh
aws s3 cp data/initialization.py s3://$BUCKET/emr/$CLUSTER_NAME/initialization.py
aws s3 cp data/zeppelin-site.xml s3://$BUCKET/emr/$CLUSTER_NAME/zeppelin-site.xml
aws s3 cp data/interpreter.json s3://$BUCKET/emr/$CLUSTER_NAME/interpreter.json
aws s3 cp data/spark-defaults-livy.conf s3://$BUCKET/emr/$CLUSTER_NAME/spark-defaults-livy.conf

python src/emr.py $AWS_PROFILE $BUCKET $CLUSTER_NAME
