# Dynamo DB
## Docs
- korean intro: https://velog.io/@drakejin/DynamoDB%EC%97%90-%EB%8C%80%ED%95%B4%EC%84%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90-1
- best practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- 
## Nosql DB
- 정형화된 스키마가 없고, 수정이 용이
- insert 쉽다
- 복잡한 조건의 조회가 어렵다.

Key
- partition key: row들의 유일한 값. used hash function
- sort key: 이걸 지정하게 되면, 동일한 partition key에 각기 다른 여러 값을 추가할 수 있는 듯
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html
  - [country]#[region]#[state]#[county]#[city]#[neighborhood] 와 같이 여러 값을 묶어서, 키로 사용하여, 특정 조건의 값을 빨리 가져올 수 있다
  - range attribute
  - sort key가 있다고 하나의 partition key에 너무 많은 데이터를 넣으면, 하나의 공간에 많은 데이터가 있게 되서, 안좋을 것 같다는 의견이 있음
  - begin_with와 같은 방식으로 조회가능. partition key의 경우, begin_with는 안된다는 것 같음.


Secondary Index
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes.html

Data Types
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html
- Scalar Types: number, string, binary, Boolean, and null
- Document type: json, list, map
- Set Types: multiple scalar values. The set types are string set, number set, and binary set.

## NoSQL workbench

## 비용
- on depand 
- provisioned
  - 매초 사용 제한이 있는 듯

## code
- awswrangler: https://github.com/aws/aws-sdk-pandas/blob/main/tutorials/028%20-%20DynamoDB.ipynb

## EMR에서 dynamodb 사용하기
- hive, hadoop, spark에서 사용하는 방식이 있음
- https://docs.aws.amazon.com/ko_kr/emr/latest/ReleaseGuide/EMRforDynamoDB.html
- https://github.com/awslabs/emr-dynamodb-connector
- https://github.com/audienceproject/spark-dynamodb
