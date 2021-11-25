# EMR
- EMR클러스터는 사용 완료 후, 종료 하는식으로 보통 쓰는 것 같음

## [Overview](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-overview.html#emr-overview-data-processing)

### Cluster
- Steps 다 처리 후, 종료할지, wait할지 선택할 수 있음
- Cluster lifecycle동안에 failure가 발생하면, cluster와 instance가 종료됨(protection mode도 있음). cluster에는 삭제 해도 되는 데이터만 저장하는게 좋을 .

### Nodes
- Master Node : 모든 작업을 관리
- Core Node : 테스크 처리 및 HDFS에 저장 (if multi-node, requires at least one)
- Task Node : 테스크만 처리.(optional)

### 작업 제출 방법
- Cluster를 생성할 때, step들을 모두 정의하는 방법
- [ ] [long-running cluster에 step을 추가하기](https://docs.aws.amazon.com/emr/latest/ManagementGuide/AddingStepstoaJobFlow.html)
- interface를 통해, 작업 제출(제플린, spark-submit)

### Step
- step output을 다음 step의 input으로 줄 수 있음
- 중간에 한 step이 실패하면, 다음 step을 지속할지, cancel할지 선택가능.
  
#### Add Steps
- [Work with Steps Using the AWS CLI and Console](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-work-with-steps.html)
- [Adding a Spark Step](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-submit-step.html)
- [AWS EMR CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/emr/create-cluster.html)
- [Create Spark Cluster by cli or java](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-launch.html)
- [zsh bug](https://github.com/Alluxio/alluxio/issues/10595)
  - use /bin/bash instead of zsh
- 여러 step을 추가할 경우, 병렬로 시작이 되고, 순차처리가 안됨(airflow dag로 순차처리하도록 처리했음) 
```shell
#!/bin/bash
aws emr add-steps \
--region ap-south-1 \
--cluster-id j-someId \
--steps Type=Spark,Name="some task",ActionOnFailure=CONTINUE,Args=[--class,com.sample.TaskExample,s3://somelink/scala-jar-file.jar,some-java-args]
```

```shell
#!/bin/bash
aws emr add-steps \
--region ap-south-1 \
--cluster-id j-someId \
--steps Type=Spark,Name="some task",ActionOnFailure=CONTINUE,Args=[--packages,io.delta:delta-core_2.12:0.8.0,--py-files,s3-path,py-file,arg1,arg2]
```
- ',' 값이 입력되어야 하면, "A\,B" 를 쓰면 됨.

```shell

aws emr create-cluster \
--name "$1" \
--log-uri "s3://bucket/$PY_NAME" \
--region ap-south-1 \
--release-label emr-6.3.0 \
--applications Name=Spark Name=Hadoop Name=Hive Name=Ganglia \
--configurations file://./spark-configuration.json \
--ec2-attributes KeyName=key-name,SubnetId=subnet-12333 \
--use-default-roles \
--instance-type m4.large --instance-count 1 --use-default-roles \
# --instance-fleets InstanceFleetType=MASTER,TargetOnDemandCapacity=1,InstanceTypeConfigs=['{InstanceType=m5.2xlarge}'] InstanceFleetType=CORE,TargetOnDemandCapacity=10,InstanceTypeConfigs=['{InstanceType=m5.xlarge}'] InstanceFleetType=TASK,TargetSpotCapacity=45,InstanceTypeConfigs=['{InstanceType=m5.2xlarge}'] \
--steps Type=Spark,Name="$1",ActionOnFailure=CONTINUE,Args=[--packages,io.delta:delta-core_2.12:0.8.0,--py-files,"s3://file.zip\,s3://file2.zip",s3://$1,live,$2] \
#--steps Type=Spark,Name="$PY_NAME",ActionOnFailure=CONTINUE,Args=[--py-files,"s3://bucket/python.zip\,s3://bucket/packages.zip",s3://bucket/$PY_NAME,live,$P1] \
--auto-terminate \
--profile A
```
- glue configuration설정을 아래와 같이 spark source code에서 해도 될듯?
```python
spark = SparkSession.builder.appName("PySparkApp")
  .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
```

### Pricing
- On-demand
- Reserved Instances
- Spot Instance 
  - It offers Significant savings(10 times less than on-demand)
  - 제플린에서 spark context가 중간에 shutdown 되는 현상이 있는데, spot instance때문이라는 의심을 하고 있음
  - Spot instance fleets + Managed auto scaling로 변경 : 기존과 같이 spot instance를 사용하기 때문에 on-demand instance를 사용하는 것 보다는 안정성이 떨어지는 것은 맞습니다.
    다만, 데이터 센터 내에 사용률이 적은 instance 종류들을 선별해서 할당될 확률을 높이고 빼앗길 확률을 최대한 낮추고자 fleeet instance를 사용하려고 하는 것입니다.
    일배치 클러스터에서 몇 번 service outage 현상을 겪은 후에 4월부터 인기 없는(?) instance들로 구성하여 fleet instance를 적용해서 운영하고 있습니다.
    현재까지는 안정적으로 운영되고 있습니다
    [참고 자료](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html)

## Usage
- zeppelin 접속은 해당 포트를 열기만 해도 됨.
    - [x] [disable anonymous](https://docs.aws.amazon.com/whitepapers/latest/teaching-big-data-skills-with-amazon-emr/step-2-disabling-anonymous-access.html)
      - 위의 문서로 하면 안됨. spark-study참조하기.
    - vpn을 통해서만 접속하게 하는 걸 권장
    - http://ec2-1-1-1-1.us-east-2.compute.amazonaws.com:8890/ 처럼 되어 있는 걸, ip 주소만 가져와서, 1.1.1.1:8890 으로 접속
- cluster hadoop 마스터 서버 접속방법
  - 22 포트 허용
  - `ssh -i {pem-file} hadoop@{master-server-ip}`
  - 클러스터의 요약 정보에 접속 방식 설명되어 있음
  ![img.png](img.png)

# SSH tunneling
## 방법
- master node 22번 포트 열기
- 아래 shell script로 port forwarding 
```
ssh -i {key-path} -ND 8157 hadoop@ip-000-000-000-000.ap-south-1.compute.internal
```
- foxyproxy로 8157 포트에 스크립트 설정 [code](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-connect-master-node-proxy.html)

## 설명
  - https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-web-interfaces.html
    - 제플린등의 port가 master node에 열려있지 않을 때, 22번 포트로 연결해서 제플린에 접속하는 방법임.
    - 단순히 제플린등의 port를 security group inbound에 등록하면 접속이 가능하지만, 보안이 취약해지므로, VPN을 쓰거나, SSH tunneling을 통해 접속하는 것을 권장. aws console에서도 url이 tunneling하는 걸 가정하고, url을 공유해주고있고, hadoop cluster monitoring에서 redirect할 때도, 이 url로 되어 있음.
    - 아래의 ssh port forwarding으로, local의 임의의 8157포트로 들어오는 데이터를 master node의 22포트로 연결
  ```shell
  # -N Do not execute a remote command.  This is useful for just for-warding ports.
  # -D Specifies a local ``dynamic'' application-level port forwarding.
  ssh -i {key-path} -ND 8157 hadoop@ip-000-000-000-000.ap-south-1.compute.internal
  ```
  - foxyproxy를 통해, 브라우저에서 접속시, local의 8157포트로 forwarding시킴.
  - 위의 두 설정을 하게 되면, foxy proxy에 의해, 마스터 노드의 특정 포트로 접속시, local의 8157포트로 전달하고, ssh port forwarding으로, 로컬의 8157포트로 들어온 데이터를 master node에 22포트로 접속하여, 8157포트로 전달하는 방식.
  - vpn을 쓴다면, vpn에서 ssh tunnel용 url을 허용해주지 않으면, ssh tunneling을 못 씀.


## Instance Fleet
- https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html
- cluster생성시 advanced option에서 설정 가능

## Error
- The EC2 Security Groups [sg-03b6c0c37c0cecce8] contain one or more ingress rules to ports other than [22] which allow public access.
  - delete the existing security groups. EMR seems to use existing security groups which is created by other EMR cluster.
  - zeppelin 접속을 위해서, inbound에 8890 포트를 열어서 그런건가?
  - ![img_1.png](img_1.png) 에서 8890을 허용해주면, security group에 8890 port를 추가했어도, 이후 cluster생성시 정상 작동하지 않을까?
- Ganglia forbidden error
  - call `sudo service httpd reload` on ssh
  - https://stackoverflow.com/questions/66064641/aws-emr-ganglia-dashboard-not-accessible-403-forbidden

- Failed to authorize instance profile EMR_EC2_DefaultRole
  - https://aws.amazon.com/ko/premiumsupport/knowledge-center/emr-default-role-invalid/
- Access
  - AmazonElasticMapReduceFullAccess
  - AmazonEMRFullAccessPolicy_v2

### EC2 instance count limit
need to request to increase the limit 
- https://ap-northeast-2.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-2#LimitsCalculator:

### EC2 instance type not supported
check if the instance type is supported on the subnet 
```shell
aws ec2 run-instances --instance-type m4.large --dry-run --image-id ami-23232323 --subnet-id subnet-123344
```

find ami id
```shell
aws ec2 describe-images --owners self amazon
```


# Performance tuning
- https://aws.amazon.com/blogs/big-data/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/

# docker
https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/016%20-%20EMR%20%26%20Docker.ipynb
- 권한 설정
  - aws cli credential에 아래 권한 추가
    - AmazonElasticMapReduceFullAccess
    - AmazonEMRFullAccessPolicy_v2
  - EMR_EC2_DefaultRole 또는 해당 role을 상속하는 role에 아래 권한 추가
    - Elastic Container Registry access
- untagged 자동 삭제
  - Lifecycle Policy 라는 걸 설정 하면, untagged 자동 삭제 가능
  - https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html


## emr log 보는 방법
- docker의 경우, stderr에 에러가 보여지지 않는다.
```
Exception in thread "main" org.apache.spark.SparkException: Application application_1637389041390_0002 finished with failed status
	at org.apache.spark.deploy.yarn.Client.run(Client.scala:1253)
	at org.apache.spark.deploy.yarn.YarnClusterApplication.start(Client.scala:1645)
	at org.apache.spark.deploy.SparkSubmit.org$apache$spark$deploy$SparkSubmit$$runMain(SparkSubmit.scala:959)
	at org.apache.spark.deploy.SparkSubmit.doRunMain$1(SparkSubmit.scala:180)
	at org.apache.spark.deploy.SparkSubmit.submit(SparkSubmit.scala:203)
	at org.apache.spark.deploy.SparkSubmit.doSubmit(SparkSubmit.scala:90)
	at org.apache.spark.deploy.SparkSubmit$$anon$2.doSubmit(SparkSubmit.scala:1047)
	at org.apache.spark.deploy.SparkSubmit$.main(SparkSubmit.scala:1056)
	at org.apache.spark.deploy.SparkSubmit.main(SparkSubmit.scala)
Command exiting with ret '1'
```
- s3에 저장되는 log를 확인하기
  - 위의 에러에 보면, `application_1637389041390_0002`라는 spark application에서 에러가 났다고 뜸
  - {해당 cluster id} -> "containers" -> {spark-application-id} -> stdout.gz 확인
- yarn등의 resource manager에서 확인하기
  - 해당 application에 들어가면, stdout 로그를 확인 가능 