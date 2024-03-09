import boto3
import os

def lambda_handler(event, context):
    regions = os.getenv("cpvi_regions", ["eu-west-3"])

    for region in regions:
        print(f"Connected to region [{region}]")

        running_instances = boto3.resource("ec2", region_name = region).instances.filter(Filters=[{"Name":"instance-state-name", "Values":["running"]}])

        for instance in running_instances:
            print(f"Checking isntance [{instance.id}]")
            should_stop = True

            if instance.tags != None:
                for tag in instance.tags:
                    if tag['Key'].lower() == "icicest" and tag['Value'].lower() == "versailles":
                        should_stop = False
                        break

            if should_stop:
                print(f"Stopping instance {instance.id}")
                instance.stop()
            else:
                print(f"Skipping instance {instance.id}")