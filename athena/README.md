# Athena

- local에서 Athena JDBC driver를 통해 Athena에 접속가능
    - https://blog.jetbrains.com/datagrip/2018/05/25/using-aws-athena-from-intellij-based-ide/
    - access 계정와 ap-south-1 처럼 위치만 있으면 됨.
- S3의 데이터를 metadata catalog를 통해 데이터 구조를 이해하여, query할 수 있음
- 아래와 같은 명령을 통해, metadata catalog의 database 안에 table을 생성하고, 해당 table을 S3의 파일과 연결가능. 아래 코드는 해당 S3파일의 데이터 구조가 어떻게 생겼는지 정의 함. 
```scala
def createTableFromFile(filePath: String, tableName: String) = {
    val schema_info = spark.read.parquet(filePath)
    val col_definition = (for (c <- schema_info.dtypes) yield(c._1 + " " + c._2.replace("Type",""))).mkString(", ")

    /**
     * hive metastore에 table을 만들고, table과 실제 데이터의 path와 연결시킴.
     */
    var createStmt = s"""CREATE EXTERNAL TABLE ${tableName}
                 (
                    ${col_definition}
                 ) STORED AS PARQUET LOCATION '$filePath'"""

    spark.sql(createStmt)
  }
  createTableFromFile("/path/to/_common_metadata", "my_table")
```

- Data source를 여러개 추가할 수 있음. 
  - 기본적으로 S3+Glue와 연동되어 있고, 다른 서비스(DynamoDB, CloudWatch)나 외부 데이터에서 가져오는게 가능
  - 다른 데이터를 가져올 때는, 람다로 쉽게 connect할 수 있는 템플릿이 있어서, 해당 템플릿에 접속방법을 설정해주고,람다를 생성 하여, 해당 데이터에 접속할 수 있게 함
  - 따라서, Athena가 하는 역할은, 어떤 데이터 소스에서든 동일한 sql로 query할 수 있게 해주는 것.

## Metadata Catalog
- AWS Glue data catalog : AWS에서 기본 제공해주는 catalog
- Apache Hive metastore

## 추가 설명
- Facebook에서 개발한 오픈소스 분산쿼리엔진인 Presto를 랩핑해서 Cloud에 구현한 것이 Athena. 따라서 Athena는 Presto 기반의 ANSI SQL을 (대부분) 지원한다.
  -> 단순히 여러 데이터 소스를 동일한 방식으로 query만 하는 것 뿐만 아니라, 분산쿼리도 가능한듯.
- S3의 데이터를 query하기 위한 interactive query service

## 특징
- serverless architecture로 사용이 간편하고 초기 비용이 저렴($5 per 1TB)
- MPP(Massive Parallel Processing)
- Performs full table scans instead of using indexes
- 다양한 데이터 소스에 연결가능

## Monitoring & Usage control

- Athena query 1회당 data scan size에 제한 및 모니터링 기준을 세팅가능, 필요에 따라 조정 가능함.
- Data scan limits : 1TB
- Data scan notification limits : 1TB per 1hour (the limit for the maximum amount of data queries are allowed to scan within a specific period.)
- 슬랙등과 연동해서, cloudwatch를 통해서 athena 알람을 받을 수 있음.

## Performance Tuning

### Partition
partitioned table 조회 시 partition 조건을 넣어주세요!
partitioned된 데이터의 경우 partition 조건을 통해 더 적은 리소스만 활용해 더 빠르게 결과를 받아볼 수 있다.

### Approximate Functions
100% 정확한 Unique Count가 필요한 케이스가 아니라면(추세를 보는 것으로 충분한 경우) distinct() 대신 approx_distinct()를 활용해 Approximate Unique Count를 활용할 수 있다.
이 방식은 hash값을 활용해 전체 string값을 읽는 것보다 훨씬 적은 메모리를 활용해 훨씬 빠르게 계산할 수 있도록 해준다. 표준오차율은 2.3%.

Example :
```sql
SELECT approx_distinct(l_comment) FROM lineitem;
```

### SELECT
asterisk(*)를 사용한 전체 선택은 지양하고 필요한 컬럼을 지정하여 SELECT

Parquet file 특성 상 컬럼별로 지정하여 원하는 컬럼만 read 하므로 불필요한 연산을 크게 줄일 수 있다.

### JOIN
Issue : Left에 작은 테이블, Right에 큰 테이블을 두면 Presto는 Right의 큰 테이블을 Worker node에 올리고 Join을 수행한다. (Presto는 join reordering을 지원하지 않음)

Best Practice : Left에 큰 테이블, Right에 작은 테이블을 두면 더 작은 메모리를 사용하여 더 빠르게 쿼리할 수 있다.

Example
Dataset: 74 GB total data, uncompressed, text format, ~602M rows

Query	Run time
```sql
SELECT count(*) FROM lineitem, part WHERE lineitem.l_partkey = part.p_partkey	//22.81 seconds
SELECT count(*) FROM part, lineitem WHERE lineitem.l_partkey = part.p_partkey	//10.71 seconds
```

### JOIN (Big Tables)
Issue : Presto는 Index 없이 fast full table scan 방식. Big table간 join은 아주 느리다. 따라서 AWS 가이드는 이런 류의 작업에 Athena 사용을 권장하지 않는다.

Best Practice : Big Table은 ETL을 통해 pre-join된 형태로 활용하는 것이 좋다.

### ORDER BY
Issue : Presto는 모든 row의 데이터를 한 worker로 보낸 후 정렬하므로 많은 양의 메모리를 사용하며, 오랜 시간 동안 수행하다가 Fail이 나기도 함.

Best Practice : 
1. LIMIT 절과 함께 ORDER BY를 사용. 개별 worker에서 sorting 및 limiting을 가능하게 해줌.
2. ORDER BY절에 String 대신 Number로 컬럼을 지정. ORDER BY order_id 대신 ORDER BY 1 

Example:
Dataset: 7.25 GB table, uncompressed, text format, ~60M rows

Query	Run time
```sql
SELECT * FROM lineitem ORDER BY l_shipdate //528 seconds
SELECT * FROM lineitem ORDER BY l_shipdate LIMIT 10000	//11.15 seconds
```


### GROUP BY
Issue : GROUPING할 데이터를 저장한 worker node로 데이터를 보내서 해당 memory의 GROUP BY값과 비교하며 Grouping한다.
Best Practice : GROUP BY절의 컬럼배치순서를 높은 cardinality부터 낮은 cardinality 순(unique count가 큰 순부터 낮은 순으로)으로 배치한다. 같은 의미의 값인 경우 가능하면 string 컬럼보다 number 컬럼을 활용해 GROUP BY한다.

Example :

```sql
SELECT state, gender, count(*) FROM census GROUP BY state, gender;
```

### LIKE
Issue : string 컬럼에 여러개의 like검색을 써야하는 경우 regular expression을 사용하는 것이 더 좋다.
Example :
```sql
SELECT count(*) FROM lineitem WHERE regexp_like(l_comment, 'wake|regular|express|sleep|hello')
```

### Compress and Split Files
Use splittable format like Apache Parquet or Apache ORC.

BZip2, Gzip로 split해서 쓰기를 권장하며 LZO, Snappy는 권장하지 않는다. (압축효율 대비 컴퓨팅 속도를 감안)

### Optimize File Size
optimal S3 file size is between 200MB-1GB (다른데서는 512mb to 1024mb라고 함)

file size가 아주 작은 경우(128MB 이하), executor engine이 S3 file을 열고, object metadata에 접근하고, directory를 리스팅하고, data transfer를 세팅하고, file header를 읽고, compression dictionary를 읽는 등의 행동을 해야하는 오버헤드로 인해 효율이 떨어지게 된다.

file size가 아주 크고 splittable하지 않은 경우, query processor는 한 파일을 다 읽을때까지 대기해야 하고 이는 athena의 강력한 parallelism 기능을 활용할 수 없게 한다.

Example

Query	Number of files	Run time
```sql
SELECT count(*) FROM lineitem	7GB, 5000 files	8.4 seconds
SELECT count(*) FROM lineitem	7GB, 1 file	2.31 seconds
```

### Join Big Tables in the ETL Layer
Athena는 index 없이 full table scan을 사용한다. 따라서 작은 규모의 데이터를 join할 때는 아무 문제 없지만 큰 데이터를 조인할 때는 ETL을 활용해 pre-join된 형태로 활용하는 것이 좋다.

### Optimize Columnar Data Store Generation
The stripe size or block size parameter : ORC stripe size, Parquet block size는 block당 최대 row수를 의미한다. ORC는 64MB, Parquet는 128MB를 default로 가진다. 효과적인 sequential I/O를 고려하여 column block size를 정의할 것.

