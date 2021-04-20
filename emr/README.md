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
```shell
#!/bin/bash
aws emr add-steps \
--region ap-south-1 \
--cluster-id j-someId \
--steps Type=Spark,Name="some task",ActionOnFailure=CONTINUE,Args=[--class,com.sample.TaskExample,s3://somelink/scala-jar-file.jar,some-java-args]
```


### Pricing
- On-demand
- Reserved Instances
- Spot Instance 
  - It offers Significant savings(10 times less than on-demand)
  - 제플린에서 spark context가 중간에 shutdown 되는 현상이 있는데, spot instance때문이라는 의심을 하고 있음

## Usage
- zeppelin 접속은 해당 포트를 열기만 해도 됨.
    - [ ] [disable anonymous](https://docs.aws.amazon.com/whitepapers/latest/teaching-big-data-skills-with-amazon-emr/step-2-disabling-anonymous-access.html)
    - vpn을 통해서만 접속하게 하는 걸 권장
- cluster hadoop 마스터 서버 접속방법
  - 22 포트 허용
  - `ssh -i {pem-file} hadoop@{master-server-ip}`
  - 클러스터의 요약 정보에 접속 방식 설명되어 있음
  ![img.png](img.png)
  

- [x] EMR에서 S3 접속하기 (자신의 s3는 기본 role에 등록되어 있음)
- [ ] glue를 통해, Hive로 sql쿼리해보기
- [ ] Athena 를 통해, s3 데이터 접근 해보기
