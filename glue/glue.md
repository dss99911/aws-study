# AWS Glue
- 메타데이터 카탈로그 서비스
- 데이터 베이스를 생성하고
- 테이블을 생성시, s3, kinesis, Kafka 등에서 데이터 소스의 위치를 정의하고, 해당 데이터의 자료 구조를 정의 함
- Athena등에서 Glue 카탈로그 서비스에서 제공하는, 데이터베이스에서 데이터를 가져와서 쿼리 할 수 있음.
- Athena는 쿼리하는 얘이고, Glue는 데이터베이스를 제공하는 얘(실제로 데이터는 Glue가 가지고 있는 건 아니지만, 데이터의 위치를 알고, 데이터의 스키마를 알기 때문에, 데이터베이스처럼 사용 가능)
- 다양한 기능이 많겠지만, 현재 알고 있는건, s3의 데이터를 데이터베이스 처럼 인식하게 하여, Athena에서 활용할 수 있게 해주는 기능

- [ ] [Dynamic Frame](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
    - similar to Dataframe but self-describing
    - glue context를통해 dynamo db에 저장할 때도 사용.