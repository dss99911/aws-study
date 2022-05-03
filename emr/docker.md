https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-docker.html
https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-docker.html#emr-docker-ECR

사용 목적
- bootstrap 으로 library설치시 시간이 걸리는데, 시간 감소 효과
- 매번 python library설치하기 위해 cluster를 종료시키고 새롭게 생성할 필요 없음


https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/016%20-%20EMR%20%26%20Docker.ipynb

- 권한 설정
    - aws cli credential에 아래 권한 추가
        - AmazonElasticMapReduceFullAccess
        - AmazonEMRFullAccessPolicy_v2
    - EMR_EC2_DefaultRole 또는 해당 role을 상속하는 role에 아래 권한 추가
        - Elastic Container Registry access


- 실행
  - spark-default에 추가하면, conf설정 안해줘도 됨
  - deploy-mode cluster에서만 작동함
    - https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.0/running-spark-applications/content/running_spark_in_docker_containers_on_yarn.html
    - pyspark-shell에서는 작동 안함
    - livy에서 쓰려면, 아래와 같이 cluster모드로 livy를 실행시켜야함. 
      - 그런데, 이렇게 하면, pyFiles설정이 안 먹힘.
      - cluster모드는 client모드와 달리, 사용되는 리소스가 커서, 처음 실행시간이 길고, 여럿이 동시 사용시 리소스 부족으로 뒤의 요청이 실행 안 될 수 있음
      - 일단 분석용 cluster는 docker를 안쓰는게 좋을듯.
```
      {
    "Classification": "livy-conf",
    "Properties": {
    "livy.spark.deploy-mode": "cluster"
    },
    "Configurations": []
    }
```