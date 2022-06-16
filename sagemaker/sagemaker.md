# Sage Maker

## sage maker 목적
- serving할 때 사용
- realtime 서빙을 하고 있을 때, 학습 용


## Auto scaling
- instance 시작하는데 시간이 걸리므로, 저사양을 여러개 하는게 좋음. 저사양이므로, 증가 조건을 낮게 설정할 수 있고, 이에 따라 점진적 증대 가능.

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

