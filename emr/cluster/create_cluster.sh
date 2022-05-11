set -e

MAX_INSTANCES=55
MAX_ONDEMAND_INSTANCES=35
MAX_CORE_INSTANCES=10

BUCKET=hyun
CLUSTER_NAME=test

aws s3 cp data/bootstrap-ds.sh s3://$BUCKET/emr/$CLUSTER_NAME/bootstrap-ds.sh
aws s3 cp data/initialization.py s3://$BUCKET/emr/$CLUSTER_NAME/initialization.py
aws s3 cp data/zeppelin-site.xml s3://$BUCKET/emr/$CLUSTER_NAME/zeppelin-site.xml
aws s3 cp data/interpreter.json s3://$BUCKET/emr/$CLUSTER_NAME/interpreter.json
aws s3 cp data/shiro.ini s3://$BUCKET/emr/$CLUSTER_NAME/shiro.ini

aws emr create-cluster \
--region ap-south-1 \
--name $CLUSTER_NAME \
--log-uri "s3://$BUCKET/emr/$CLUSTER_NAME/logs" \
--release-label emr-6.6.0 \
--applications Name=Hadoop Name=Spark Name=Zeppelin Name=Hive Name=Livy Name=JupyterEnterpriseGateway \
--configurations file://./data/spark-configuration.json \
--ec2-attributes KeyName=hyun,SubnetId=subnet-1 \
--use-default-roles \
--managed-scaling-policy '{"ComputeLimits":{"MaximumOnDemandCapacityUnits":'$MAX_ONDEMAND_INSTANCES',"UnitType":"Instances","MaximumCapacityUnits":'$MAX_INSTANCES',"MinimumCapacityUnits":1,"MaximumCoreCapacityUnits":'$MAX_CORE_INSTANCES'}}' \
--scale-down-behavior TERMINATE_AT_TASK_COMPLETION \
--instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m5.xlarge \
                  InstanceGroupType=CORE,InstanceCount=1,InstanceType=m5.xlarge \
                  InstanceGroupType=TASK,InstanceCount=1,InstanceType=m5.2xlarge \
                  InstanceGroupType=TASK,InstanceCount=1,InstanceType=c5.2xlarge,BidPrice=0.5 \
--bootstrap-actions Name='Bootstrap action',Path="s3://$BUCKET/emr/$CLUSTER_NAME/bootstrap.sh" \
--steps Type=Spark,Name='initialization',ActionOnFailure=CONTINUE,Args=s3://$BUCKET/emr/$CLUSTER_NAME/initialization.py
