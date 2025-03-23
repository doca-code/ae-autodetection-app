from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    RemovalPolicy
)

class DevInstanceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        new_vpc = ec2.Vpc(self, "VPC")

        # IAM Role for EC2 (Allows SSM & Basic Access)
        role = iam.Role(
            self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )
        role.apply_removal_policy(RemovalPolicy.DESTROY)

        # Create the EC2 instance
        instance = ec2.Instance(
            self, "DevInstance",
            instance_type=ec2.InstanceType("t3.large"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=new_vpc,
            role=role,
        )

        # User Data to set up the instance
        instance.user_data.add_commands(
            "yum update -y",
            "yum install -y unzip git python3-pip",  # Install dependencies (git, unzip, pip)
            "cd /home/cloudshell-user",
            "git clone https://github.com/doca-code/ae-autodetection-app.git",  # Clone the full repo
            "cd ae-autodetection-app/data_ingestion",
            "unzip data_ingestion.zip -d ../twitter-scripts",  # Extract ZIP into twitter-scripts folder
            "rm data_ingestion.zip",  # Clean up ZIP file
        )
        # Make sure VPC is deleted when the stack is destroyed
        new_vpc.apply_removal_policy(RemovalPolicy.DESTROY)
