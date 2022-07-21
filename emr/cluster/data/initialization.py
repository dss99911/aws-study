import os
import sys


def main(bucket, cluster_name, gpu, do_test):
    spark = initialize_spark(do_test)
    configure_python()
    configure_zeppelin(bucket, cluster_name)
    configure_livy(bucket, cluster_name)
    if do_test == "true":
        test(spark, bucket, cluster_name, gpu)


def initialize_spark(do_test):
    # at first spark initialization, download libraries. and it takes long time.
    return (
        SparkSession.builder.appName("initialization")
        .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")
        .enableHiveSupport()
        .getOrCreate()
    )


def configure_python():
    # emr numpy version is too old to use awswrangler. and emr install numpy after bootstrapping.
    # so, run this code after emr install numpy.
    os.system("sudo python3 -m pip install -U --ignore-installed numpy")


def configure_zeppelin(bucket, cluster_name):
    os.system(f"sudo aws s3 cp s3://{bucket}/emr/{cluster_name}/zeppelin-site.xml /etc/zeppelin/conf.dist/zeppelin-site.xml")
    os.system(f"sudo aws s3 cp s3://{bucket}/emr/{cluster_name}/shiro.ini /etc/zeppelin/conf.dist/shiro.ini")

    # it doesn't work on bootstrap. so, running on initialization
    os.system(f"sudo aws s3 cp s3://{bucket}/emr/{cluster_name}/interpreter.json /home/hadoop/interpreter.json")

    def replace_hostname(path, new_path):
        import socket
        hostname = socket.gethostname()

        def read_file(file_path):
            with open(file_path, 'r') as f:
                return f.read()

        def write_file(file_path, data):
            with open(file_path, 'w') as f:
                f.write(data)

        interpreter_json = read_file(path)
        interpreter_json = interpreter_json.replace("ip-1-1-1-1", hostname)
        write_file(new_path, interpreter_json)

    replace_hostname("/home/hadoop/interpreter.json", "/home/hadoop/interpreter_new.json")
    os.system("sudo cp /home/hadoop/interpreter_new.json /etc/zeppelin/conf.dist/interpreter.json")
    os.system("sudo rm /home/hadoop/interpreter.json /home/hadoop/interpreter_new.json")
    os.system("sudo service zeppelin restart")


def configure_livy(bucket, cluster_name):
    # livy ignore pyFiles on spark-conf/spark-defaults,
    os.system(f"sudo aws s3 cp s3://{bucket}/emr/{cluster_name}/spark-defaults-livy.conf /etc/livy/conf.dist/spark-defaults.conf")


def test(spark, bucket, cluster_name, gpu):
    test_pandas_udf(spark)
    test_torch(spark, gpu)
    test_nlp(gpu)
    if gpu == 'true':
        test_synapseML(spark, bucket, cluster_name)
    test_livy()


def test_pandas_udf(spark):
    from pyspark.sql.functions import pandas_udf
    import pandas as pd

    df = spark.createDataFrame(
        [(1, 1.0), (1, 2.0), (2, 3.0), (2, 5.0), (2, 10.0)],
        ("id", "v"))

    @pandas_udf("double")
    def mean_udf(v: pd.Series) -> float:
        return v.mean()

    print(df.groupby("id").agg(mean_udf(df['v'])).collect())


def test_torch(spark, gpu):
    import torch
    x = torch.rand(5, 3)
    print(x)

    def is_cuda(a):
        return torch.cuda.is_available()

    assert spark.sparkContext.parallelize(range(1, 10)).map(is_cuda).distinct().collect() == [gpu == "true"]


def test_nlp(gpu):
    import sparknlp
    from sparknlp.pretrained import PretrainedPipeline
    spark = sparknlp.start(gpu == 'true')
    sparknlp.start()
    sentences = [
        ['Hello, this is an example sentence'],
        ['And this is a second sentence.']
    ]

    # spark is the Spark Session automatically started by pyspark.
    data = spark.createDataFrame(sentences).toDF("text")

    # Download the pretrained pipeline from Johnsnowlab's servers
    explain_document_pipeline = PretrainedPipeline("explain_document_ml")


def test_synapseML(spark, bucket, cluster_name):
    # https://microsoft.github.io/SynapseML/docs/next/features/lightgbm/LightGBM%20-%20Overview/
    df = (
        spark.read.format("csv")
        .option("header", True)
        .option("inferSchema", True)
        .load(
            f"s3://{bucket}/emr/{cluster_name}/company_bankruptcy_prediction_data.csv"
        )
    )
    print("records read: " + str(df.count()))
    print("Schema: ")
    df.printSchema()

    train, test = df.randomSplit([0.85, 0.15], seed=1)

    from pyspark.ml.feature import VectorAssembler

    feature_cols = df.columns[1:]
    featurizer = VectorAssembler(inputCols=feature_cols, outputCol="features")
    train_data = featurizer.transform(train)["Bankrupt?", "features"]
    test_data = featurizer.transform(test)["Bankrupt?", "features"]

    from synapse.ml.lightgbm import LightGBMClassifier

    model = LightGBMClassifier(
        objective="binary", featuresCol="features", labelCol="Bankrupt?", isUnbalance=True
    )

    model = model.fit(train_data)
    model.getFeatureImportances()


def test_livy():
    import requests
    import json
    import time

    server_ip = 'http://localhost'
    headers = {'Content-Type': 'application/json'}

    # create session
    data = {'kind': 'spark'}
    url = f'{server_ip}:8998/sessions'
    response = requests.post(url, data=json.dumps(data), headers=headers)
    session_id = response.json()['id']

    def wait_idle(count):
        if count <= 0:
            raise ValueError("time out for livy")
        url = f'{server_ip}:8998/sessions/{session_id}'
        response = requests.get(url, headers=headers)
        if response.json()["state"] != "idle":
            time.sleep(1)
            wait_idle(count - 1)

    wait_idle(300)

    # run code
    data = {'code': 'spark'}
    url = f'{server_ip}:8998/sessions/{session_id}/statements'
    response = requests.post(url, data=json.dumps(data), headers=headers)
    statement_id = response.json()['id']

    wait_idle(300)

    # check statement output
    url = f'{server_ip}:8998/sessions/{session_id}/statements/{statement_id}'
    response = requests.get(url, headers=headers)

    assert response.json()['output']['status'] == 'ok'

    # delete session
    url = f'{server_ip}:8998/sessions/{session_id}'
    response = requests.delete(url, headers=headers)
    response.json()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
