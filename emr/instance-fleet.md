# Instance fleet

## references
- https://aws.amazon.com/ko/blogs/korea/new-amazon-emr-instance-fleets/
- https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html


## configs

### fleet config
- TargetSpotCapacity
- TargetOnDemandCapacity
- LaunchSpecifications.SpotSpecification
  - TimeoutDurationMinutes : 스팟 인스턴스 생성 시간 제한
  - TimeoutAction: SWITCH_TO_ON_DEMAND 여부 결정


#### InstanceTypeConfigs
각 fleet별 여러 instance type을 설정할 수 있다.
- InstanceType
- BidPriceAsPercentageOfOnDemandPrice: 100은 demand와 같은 가격으로 생성 
- WeightedCapacity: 각 instance type별 weight를 설정할 수 있다.


## create cluster
fleet 설정을 json으로 설정가능
```shell
aws emr create-cluster --release-label emr-5.4.0 \
--applications Name=Spark,Name=Hive,Name=Zeppelin \
--service-role EMR_DefaultRole \
--ec2-attributes InstanceProfile="EMR_EC2_DefaultRole,SubnetIds=[subnet-1143da3c,subnet-2e27c012]" \
--instance-fleets file://my-fleet-config.json
```