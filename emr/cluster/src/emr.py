import sys

import boto3
from cheapest_spot_instance_retriever import get_cheapest_instance_types
import json

_region = "ap-south-1"
_emr_release_ver = "emr-6.6.0"
_subnet_id = "subnet-1"
_key_pair_name = "hyun"
_tags = {"Service": "cluster", "Application": "emr"}
_applications = ["Hadoop", "Spark", "Hive", "Zeppelin", "Ganglia", "Livy", "JupyterEnterpriseGateway"]


def process(profile, bucket, cluster_name):
    boto3.setup_default_session(region_name=_region, profile_name=profile)
    run_emr_spark_job_fleet(
        bucket=bucket,
        cluster_name=cluster_name,
        name=cluster_name,
        steps=[build_spark_step_fleet(
            path=f"s3://{bucket}/emr/{cluster_name}/initialization.py",
            name=f"initialization"
        )],
        instance_fleets=get_cheapest_spot_instance_fleets(
            available_categories=["r"],
            min_ram=7,
            core_instance_type="r5.xlarge"
        ),
        maximum_on_demand_capacity_units=1,
        maximum_capacity_units=100,
        logging_s3_path=f"s3://{bucket}/emr/{cluster_name}/logs",
        configuration=load_json_from_file("data/spark-configuration.json")
    )


def run_emr_spark_job_fleet(
        bucket,
        cluster_name,
        name: str,
        steps: list,
        instance_fleets,
        maximum_on_demand_capacity_units=10,
        maximum_capacity_units=200,
        logging_s3_path=None,
        configuration=None,
):
    connection = boto3.client('emr')

    response = connection.run_job_flow(
        Name=name,
        LogUri=logging_s3_path,
        ReleaseLabel=_emr_release_ver,
        Applications=[{'Name': app} for app in _applications],
        Instances={
            'InstanceFleets': instance_fleets,
            'Ec2KeyName': _key_pair_name,
            'KeepJobFlowAliveWhenNoSteps': True,
            'Ec2SubnetId': _subnet_id,
        },
        ManagedScalingPolicy={
            "ComputeLimits": {
                "MaximumOnDemandCapacityUnits": maximum_on_demand_capacity_units,
                "UnitType": "InstanceFleetUnits",
                "MaximumCapacityUnits": maximum_capacity_units,
                "MinimumCapacityUnits": 1,
                "MaximumCoreCapacityUnits": 1
            }
        },
        ScaleDownBehavior='TERMINATE_AT_TASK_COMPLETION',
        Configurations=configuration,
        Steps=steps,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
        BootstrapActions=[
            {
                'Name': f'{cluster_name} Bootstrap action',
                'ScriptBootstrapAction': {
                    'Path': f's3://{bucket}/emr/{cluster_name}/bootstrap.sh',
                }
            },
        ],
        Tags=[{'Key': k, 'Value': v} for k, v in _tags.items()]
    )
    cluster_id = response['JobFlowId']
    print(f"Cluster ID: {cluster_id}")


def build_spark_step_fleet(
        name,
        path: str,
):
    return {
        'Name': name,
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                *path.split(" ")
            ]

        }
    }


def get_cheapest_spot_instance_fleets(
        available_categories=["m"],
        max_frequency=1,
        min_ram=3,
        min_cores=4,
        max_cores=32,
        min_saving_ratio=70,
        limit=8,
        master_instance_type="m5.xlarge",
        core_instance_type="m5.xlarge",
        ebs_size=128,
        bid_percent=50
):
    master_fleet = {
        "Name": "Masterfleet",
        "InstanceFleetType": "MASTER",
        "TargetOnDemandCapacity": 1,
        "InstanceTypeConfigs": [
            {
                "WeightedCapacity": 1,
                "EbsConfiguration": {"EbsBlockDeviceConfigs": [{"VolumeSpecification": {"SizeInGB": ebs_size, "VolumeType": "gp2"}, "VolumesPerInstance": 1}]},
                "InstanceType": master_instance_type
            }
        ],
    }

    core_fleet = {
        "Name": "Corefleet",
        "InstanceFleetType": "CORE",
        "TargetOnDemandCapacity": 1,
        "InstanceTypeConfigs": [
            {
                "WeightedCapacity": 1,
                "EbsConfiguration": {"EbsBlockDeviceConfigs": [{"VolumeSpecification": {"SizeInGB": ebs_size, "VolumeType": "gp2"}, "VolumesPerInstance": 1}]},
                "InstanceType": core_instance_type}
        ]
    }

    task_df = get_cheapest_instance_types(
        region=_region,
        available_categories=available_categories,
        max_frequency=max_frequency,
        min_ram=min_ram,
        min_cores=min_cores,
        max_cores=max_cores,
        min_saving_ratio=min_saving_ratio,
        limit=limit
    )

    def get_task_instance_dict(instance_row):
        instance_type = instance_row[0]
        weight = int(instance_row[1]["cores"] / 4)
        return {
            "WeightedCapacity": weight,
            "EbsConfiguration": {
                "EbsBlockDeviceConfigs": [
                    {
                        "VolumeSpecification": {
                            "SizeInGB": ebs_size,
                            "VolumeType": "gp2"},
                        "VolumesPerInstance": weight}]},
            "BidPriceAsPercentageOfOnDemandPrice": bid_percent,
            "InstanceType": instance_type
        }

    task_fleet = {
        "Name": "Taskfleet",
        "InstanceFleetType": "TASK",
        "TargetOnDemandCapacity": 0, "TargetSpotCapacity": 1,
        "LaunchSpecifications": {
            "SpotSpecification": {"TimeoutDurationMinutes": 10, "AllocationStrategy": "CAPACITY_OPTIMIZED",
                                  "TimeoutAction": "SWITCH_TO_ON_DEMAND"}
        },
        "InstanceTypeConfigs": [get_task_instance_dict(row) for row in task_df.iterrows()],
    }

    return [master_fleet, core_fleet, task_fleet]


def load_json_from_file(path):
    f = open(path, 'r')
    return json.load(f)  # load json from file o


if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2], sys.argv[3])
