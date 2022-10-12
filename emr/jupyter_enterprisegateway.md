# Jupyter Enterprise Gateway

## python에서 spark 연결하기
```python
import os
import findspark
findspark.init()
import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
os.environ['PYSPARK_SUBMIT_ARGS'] = """
    --name attaching_glue
    --conf spark.pyspark.virtualenv.enabled=true
    --conf spark.pyspark.virtualenv.type=native
    --conf spark.pyspark.virtualenv.bin.path=/usr/bin/virtualenv
    --conf spark.dynamicAllocation.enabled=True
    --conf spark.shuffle.service.enabled=True
    --conf spark.dynamicAllocation.maxExecutors=10
    --conf spark.dynamicAllocation.initialExecutors=2
    --conf spark.dynamicAllocation.executorIdleTimeout=5s
    --conf spark.executor.memory=10g
    --conf spark.executor.cores=2
    --conf spark.driver.memory=10g
    --conf spark.driver.cores=2
    --conf spark.sql.shuffle.partitions=50
    --conf spark.driver.maxResultSize=10g
    --conf spark.executor.memoryOverhead=2g
    --conf spark.sql.execution.arrow.enabled=True
    --conf spark.sql.execution.arrow.fallback.enabled=True
    --conf spark.sql.broadcastTimeout=3000000
    --conf spark.sql.caseSensitive=True
    --conf fs.s3a.fast.upload=True
    --conf spark.sql.execution.arrow.pyspark.enabled=True
    --conf spark.sql.legacy.parquet.datetimeRebaseModeInRead=LEGACY
    --conf spark.sql.legacy.parquet.datetimeRebaseModeInWrite=LEGACY
    --conf hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory
    pyspark-shell"""
spark = pyspark.sql.SparkSession.builder.getOrCreate()
sc = spark.sparkContext
sess = SparkSession.builder.enableHiveSupport().getOrCreate()
spark

```

## 로컬에서 EMR jupyter enterprisegateway 연결하기

EMR 설정
- nginx
    - 18888포트로 접속시, enterprisegateway로 redirect 시켜준다
    - ssl cert 가 설정 되어 있음


접속
1. jupyter lab --gateway-url=https://xxx:18888
    - ssl certifate이 없어서 에러남

2. curl https://xxx:18888 ---cacert {crt-file}
    - emr cluster master노드에서 crt 파일을 다운 받을 수 있음(nginx.conf에 위치 명시)
    - ssl cert의 도메인 명이 localhost로 되어 있어, 접근 에러남

3. ssh port forwarding
    - ssh -i {key-file} -N -L 18888:localhost:18888 hadoop@{server-ip}
    - 위의 코드를 통해, localhost:18888로 접속시, 서버에서 18888로 접속하게 함
    - curl https://localhost:18888 ---cacert {crt-file} 를 할 경우, 접속 성공

4. jupyter lab --gateway-url=https://xxx:18888 --certfile {crt-file}
    - curl은 접속 성공 했지만, jupyter에서는 여전히 에러남.
    - crt-file을 pem으로 변환해도 마찬가지

5. certification를 맥에 설치
    - crt파일 더블클릭
    - 인증서중에 localhost로 검색
    - 더블클릭해서 항상 허용으로 변경
    - https://medium.com/analytics-vidhya/get-rid-of-ssl-errors-with-jupyter-notebooks-1a80dd509988
    - curl https://localhost:18888 로 crt file지정하지 않아도 접속 가능
    - jupyter는 여전히 에러 발생

6. export SSL_CERT_FILE=nginx.crt
    - https://gentlesark.tistory.com/76
    - 이 방법을 시도하니, 정상 작동(certification 설치 안해도 됨)


요약
- ssh -i {key-file} -N -L 18888:localhost:18888 hadoop@{server-ip}
- export SSL_CERT_FILE=nginx.crt
- jupyter lab --gateway-url=https://xxx:18888