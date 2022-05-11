set -e

BUCKET=hyun
CLUSTER_NAME=test_rapid

aws s3 cp data/bootstrap-rapid.sh s3://$BUCKET/emr/$CLUSTER_NAME/bootstrap-rapid.sh
aws s3 cp data/initialization_rapid.py s3://$BUCKET/emr/$CLUSTER_NAME/initialization_rapid.py

MAX_INSTANCES=4
MAX_ONDEMAND_INSTANCES=2
MAX_CORE_INSTANCES=1

aws emr create-cluster \
--region ap-south-1 \
--name $CLUSTER_NAME \
--log-uri "s3://$BUCKET/emr/$CLUSTER_NAME/rapid_logs" \
--release-label emr-6.6.0 \
--applications Name=Hadoop Name=Spark Name=Zeppelin Name=Hive Name=Livy Name=JupyterEnterpriseGateway \
--configurations file://./data/spark-configuration-rapid.json \
--ec2-attributes KeyName=hyun,SubnetId=subnet-1 \
--use-default-roles \
--managed-scaling-policy '{"ComputeLimits":{"MaximumOnDemandCapacityUnits":'$MAX_ONDEMAND_INSTANCES',"UnitType":"Instances","MaximumCapacityUnits":'$MAX_INSTANCES',"MinimumCapacityUnits":1,"MaximumCoreCapacityUnits":'$MAX_CORE_INSTANCES'}}' \
--scale-down-behavior TERMINATE_AT_TASK_COMPLETION \
--instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.4xlarge \
                  InstanceGroupType=CORE,InstanceCount=1,InstanceType=g4dn.2xlarge \
                  InstanceGroupType=TASK,InstanceCount=1,InstanceType=g4dn.2xlarge \
                  InstanceGroupType=TASK,InstanceCount=1,InstanceType=g4dn.2xlarge,BidPrice=0.5 \
--bootstrap-actions Name='Rapid Bootstrap action',Path="s3://$BUCKET/emr/$CLUSTER_NAME/bootstrap-rapid.sh" \
--steps Type=Spark,Name='initialization',ActionOnFailure=CONTINUE,Args=s3://$BUCKET/emr/$CLUSTER_NAME/initialization_rapid.py \
--auto-termination-policy IdleTimeout=3600
