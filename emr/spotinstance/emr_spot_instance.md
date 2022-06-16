# Spot instance
- 가격은 싸지만, 중간에 인스턴스가 반환되어, 작업 중 이던게 사라질 수 있음

## 작업상 고려사항
- task를 작게 분할하여, 큰 작업이 도중에 중단되지 않게 하기
  - 작업 partition 수
  - spark.sql.shuffle.partitions 수
  - 노는 core수를 줄여서, core들을 충분히 사용할 수 있음
- 중간에 s3, hdfs에 저장
- persist(StorageLevel.DISK_ONLY_2)로 한 instance 가 꺼져도, 중간 데이터가 남도록 처리
- 

## Spot instance 선정
- https://aws.amazon.com/ec2/spot/instance-advisor/ 에 비용절감이 크고, interruption이 적은 spot instance를 찾을 수 있다.
- [cheapest_spot_instance_retriever.py](cheapest_spot_instance_retriever.py)를 통해, 최저가 spot instance를 찾을 수 있다.
- memory / core 비율이 비슷한 걸 써야, 메모리를 충분히 사용할 수 있 (executor.memory는 emr에서 가장 작은 instance의 값으로 자동 설정됨)
- core가 많은 instance는 interruption 발생시 피해가 크므로, 적당히 적은 core의 인스턴스를 많이 쓰는게 중요.
- 

## create EMR cluster
- instance fleet으로 여러 싼 spot instance를 설정한다
- 기본 instance 수는 작게 하고, ManagedScalingPolicy로 MaximumCapacityUnits 설정하여, provisioning을 빨리 할 수 있게 한다.
- bid 비율은 50%로
- core 갯수로, ebs 갯수 및, capacity weight설정