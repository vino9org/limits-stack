import os

import boto3
import pytest
from botocore.exceptions import ClientError


@pytest.fixture(scope="session", autouse=True)
def api_base_url() -> str:
    region = os.environ.get("TESTING_REGION", "us-west-2")
    stack_name = os.environ.get("TESTING_STACK_NAME", "LimitsStack")
    client = boto3.client("cloudformation", region_name=region)

    try:
        response = client.describe_stacks(StackName=stack_name)
    except ClientError as e:
        raise Exception(f"Cannot find stack {stack_name} in region {region}") from e

    stack_outputs = response["Stacks"][0]["Outputs"]
    api_outputs = [item for item in stack_outputs if "RestApiEndpoint" in item["OutputKey"]]
    return api_outputs[0]["OutputValue"]
