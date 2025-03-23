#!/usr/bin/env python3
import aws_cdk as cdk
import boto3

from stack.s3_stack import S3Stack
from stack.ae_stack import AeStack 

region_name = boto3.session.Session().region_name
env={'region': region_name}

app = cdk.App()
#vpc_stack = AiVpcNetworkStack(app, "VPCStack", env=env)

ae_bucket = S3Stack(app, "ae-bucket-east-1", env=env) #self, stack name, env=region
AeStack(app, "ae-east-1", bucket=ae_bucket.bucket, env=env)

app.synth()
