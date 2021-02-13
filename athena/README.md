# Athena

- local에서 Athena JDBC driver를 통해 Athena에 접속가능
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

## Metadata Catalog
- AWS Glue data catalog : AWS에서 기본 제공해주는 catalog
- Apache Hive metastore