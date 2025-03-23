from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_sagemaker as sagemaker,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_glue as glue,
    aws_lambda_event_sources as lambda_event_sources,
    App, Stack  # Core is part of aws-cdk-lib now in CDK v2
)

from .modeling_stack import AeModelStack
from .dynamodb_stack import TweetsTable
from .glue_stack import GlueStack
AE_THRESHOLD = "0.6"

SAGEMAKER_ENDPOINT_NAME = "HF-BERT-AE-model"  # Set as global variable

class AeStack(Stack):

    def __init__(self, scope: App, construct_id: str, bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Model Training and Deployment 
        ## SageMaker Resources
        AeModelStack(self, 'AEModeling-east-1', bucket_name=bucket.bucket_name) 

        # Inference pipeline
        ## DynamoDB for recording streaming tweets
        tweets_processer = TweetsTable(
            self, 'TweetsWrittenByLambda-east-1', table_name="ae_tweets_ddb",
            AE_THRESHOLD=AE_THRESHOLD, bucket_name=bucket.bucket_name)

        # Grant read write access to AWS Glue Crawler
        bucket.grant_read_write(tweets_processer.handler)
        
        # Glue Stack for Crawling data
        GlueStack(self, "GlueCrawler-east-1", bucket.bucket_name)

