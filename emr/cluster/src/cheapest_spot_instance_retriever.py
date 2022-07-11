
import boto3
from datetime import datetime, timedelta

import requests
import pandas as pd
from functools import reduce


def get_cheapest_instance_types(region, available_categories=None, max_frequency=None, min_ram=None, min_cores=None, max_cores=None, min_saving_ratio=None, limit=None):
    """
    :param region:
    :param available_categories: ["m", "c", "r", "p", "g", "i"] or etc. if None, doesn't filter by category
    :param max_frequency: 0: <5%, 1: 5-10%, 2: 10-15%, 3: 15-20%, 4: >20%
    :param min_ram: an instance's minimum memory in GB
    :param min_cores: an instance's minimum core
    :param max_cores: an instance's maximum core
    :param min_saving_ratio:
    :param limit: instance limits
    :return:
    """
    df_spot = get_spot_instance_data(region)
    df_spot = df_spot[
        df_spot["emr"]
        & ((df_spot["frequency_interrupt"] <= max_frequency) if max_frequency else True)  # average value in month
        & ((df_spot["ram_gb"] / df_spot["cores"] >= min_ram) if min_ram else True)
        & ((df_spot["cores"] >= min_cores) if min_cores else True)
        & ((df_spot["cores"] <= max_cores) if max_cores else True)
        & (is_in_categories(df_spot, available_categories) if available_categories else True)
        ]
    df_spot["recent_saving_ratio"] = get_recent_saving_ratio(df_spot, region)

    if min_saving_ratio:
        df_spot = df_spot[df_spot["recent_saving_ratio"] >= min_saving_ratio]

    # as max_frequency index increased by 5%
    df_spot["score"] = df_spot["recent_saving_ratio"] - df_spot["frequency_interrupt"] * 5

    # get the top n instances by score
    df_spot = df_spot.sort_values("score", ascending=False)

    if limit:
        df_spot = df_spot.head(limit)

    return df_spot


def is_in_categories(df_spot, categories):
    conds = [df_spot.index.str.startswith(c) for c in categories]
    return reduce(lambda a, b: a | b, conds, False)


def get_recent_saving_ratio(df_spot, region):
    instance_types = list(df_spot.index)
    spot_prices = get_spot_price(instance_types, region)
    on_demand_prices = get_on_demand_prices(instance_types, region)
    df_spot["spot_price"] = df_spot.index.map(lambda x: spot_prices.get(x))
    df_spot["on_demand_price"] = df_spot.index.map(lambda x: on_demand_prices.get(x) if x != "r3.xlarge" else on_demand_prices.get("r5.xlarge"))  # r3.xlarge doesn't exist in on_demand_prices
    return (df_spot["on_demand_price"] - df_spot["spot_price"]) / df_spot["on_demand_price"] * 100


def get_spot_instance_data(aws_region):
    spot_data = requests.get("https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json").json()
    instance_types_dict: dict = spot_data["instance_types"]
    spot_advisor_dict = spot_data["spot_advisor"][aws_region]["Linux"]

    emr_instance_types = {k for k, v in instance_types_dict.items()}
    region_instance_types = {k for k, v in spot_advisor_dict.items()}

    def get_values(instance_type):
        instance = instance_types_dict[instance_type]
        spot_advisor = spot_advisor_dict[instance_type]
        return {
            "instance_type": instance_type,
            "emr": instance["emr"],
            "cores": instance["cores"],
            "ram_gb": instance["ram_gb"],
            "frequency_interrupt": spot_advisor["r"],
            "saving_ratio": spot_advisor["s"]
        }

    return pd.DataFrame.from_dict([
        get_values(instance_type) for instance_type in emr_instance_types & region_instance_types
    ]).set_index("instance_type")


def get_spot_price(instance_types, aws_region):
    start = datetime.now() - timedelta(days=1)

    ec2_client = boto3.client('ec2', aws_region)
    price_dict = ec2_client.describe_spot_price_history(
        StartTime=start,
        InstanceTypes=instance_types,
        ProductDescriptions=['Linux/UNIX (Amazon VPC)']
    )

    instance_type_price_dict = {}
    histories = sorted(price_dict["SpotPriceHistory"], key=lambda x: x["Timestamp"])
    for history in histories:
        instance_type_price_dict[history["InstanceType"]] = float(history["SpotPrice"])

    return instance_type_price_dict


def get_on_demand_prices(instance_types, region):
    regions = {
        "ap-south-1": "Asia%20Pacific%20(Mumbai)"
    }

    now_in_millis = int(datetime.now().timestamp() * 1000)
    instance_data = requests.get(f"https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/{regions[region]}/Linux/index.json?timestamp={now_in_millis}").json()

    prices = {v["Instance Type"]: float(v["price"]) for v in list(instance_data["regions"].values())[0].values() if v["Instance Type"] in instance_types}
    return prices


if __name__ == '__main__':
    result = get_cheapest_instance_types(
        region="ap-south-1",
        available_categories=["r"],
        max_frequency=3,
        min_ram=7,
        min_cores=1,
        max_cores=32,
        min_saving_ratio=70,
        limit=10
    )
