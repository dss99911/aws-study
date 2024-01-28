# Sage Maker

## sage maker 목적
- serving할 때 사용
- realtime 서빙을 하고 있을 때, 학습 용


## Auto scaling
### 저사양 instance
    - instance 시작하는데 시간이 걸리므로, 저사양을 여러개 하는게 좋음. 저사양이므로, 증가 조건을 낮게 설정할 수 있고, 이에 따라 점진적 증대 가능.
    - 저사양으로 할 경우, 1개 request처리시, 더 오랜 시간이 걸릴 수도 있으므로, latency도 고려해서, 설정

### Scaling policy
#### CPU usage
#### invocation per instance
#### model latency
- scaling의 궁극적 목적은 model latency를 적정선으로 유지하는 것에 있다.
- 하지만, model latency는 처리가 다 끝난 다음에 알 수 있는 값이라서, invocation수 처럼, invocation이 일어나는 시점에 알 수 있는 값이나, cpu usage와 같은 처리 도중에 알 수 있는 값에 비해, scaling이 늦어질 수 밖에 없다.

### scaling activity log
on alarm tap of endpoint console, able to see when scaling occurred. but can't see the instance count

able to see the instance count
```shell
#aws application-autoscaling describe-scaling-activities --service-namespace sagemaker --resource-id endpoint/{endpoint-name}/variant/AllTraffic >> endpoint-2023-09-08.json
```

## Metric
### Sagemaker endpoint instance count
log insights
```
fields @timestamp, @message
| filter @logStream like "AllTraffic"
| parse @logStream "AllTraffic*" as InstanceId
| stats count_distinct(InstanceId) as InstanceCount by bin(5m)
```

## Spark
https://github.com/aws/sagemaker-spark/blob/master/README.md
- pip install sagemaker_pyspark
- 
https://docs.aws.amazon.com/sagemaker/latest/dg/apache-spark.html


## Pricing
https://aws.amazon.com/ko/sagemaker/pricing/


## Sagemaker Project
장점
- 사람이 빌드하는게 아니라, 시스템이 빌드부터 배포까지 진행 (실수 방지)
- 커밋만으로 배포 가능(개발은 별도 브랜치에서 하고, 최종 master브랜치에 머지시 자동 배포)
- repo, 파이프라인, 모델, endpoint를 한 곳에서 관리 가능

단점
- 여러 모델을 하나의 프로젝트에서 관리하기 애매(하나 커밋시마다, 여러 모델의 파이프라인에 영향)

결론
- 독립적인 모델의 경우 sagemaker project를 써도 좋을 것 같지만, 여러 모델이 동일 코드를 공용으로 사용하는 것이 많아. 사용하기 어려워 보임
- 장점이 별로 크지 않아 보이고, 젠킨스에서도 가능해 보임
- Model Registry와 pipeline을 좀더 체계적으로 사용하는 정도만 하면 좋을 것 같음

