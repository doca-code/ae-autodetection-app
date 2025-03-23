from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy
)
from constructs import Construct

class S3Stack(Stack):
    @property
    def bucket(self):
        return self._bucket  

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 Bucket for AI model artifacts and notebooks
        self._bucket = s3.Bucket(
            self, "AEModelingBucket-east-1", 
            bucket_name=f"ae-modeling-bucket-49002342303234-east-1",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY, 
            auto_delete_objects=True,  # Ensures cleanup upon stack deletion
        )

        # Upload SageMaker notebooks from local to S3
        s3deploy.BucketDeployment(
            self, 'UploadModelingFiles-east-1',
            sources=[s3deploy.Source.asset('sagemaker')],
            destination_bucket=self._bucket,
            destination_key_prefix='sagemaker'
        )
