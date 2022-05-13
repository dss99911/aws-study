from ds_common_utils.pyspark.all import *
import os


def main():
    initialize_spark()
    configure_livy()


def initialize_spark():
    # at first spark initialization, download libraries. and it takes long time.
    spark = SparkSession.builder.appName("PySparkApp") \
        .config("hive.metastore.client.factory.class", "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory") \
        .enableHiveSupport() \
        .getOrCreate()


def configure_livy():
    # livy ignore pyFiles on spark-conf/spark-defaults,
    os.system("sudo aws s3 cp spark-defaults-livy.conf /etc/livy/conf.dist/spark-defaults.conf")


if __name__ == '__main__':
    main()