from constructs import Construct
from aws_cdk import (
    aws_sagemaker as sagemaker,
    aws_iam as iam,
    aws_ec2 as ec2,
    Fn,
    RemovalPolicy
)


class AeModelStack(Construct):

    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._PREFIX = construct_id

        # Create Role for the SageMaker Backend
        self._service_role = iam.Role(
            self, f'{self._PREFIX}-ServiceRole-east-1',
            role_name=f'{self._PREFIX}-ServiceRole-east-1',
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("sagemaker.amazonaws.com"),
                iam.ServicePrincipal("lambda.amazonaws.com"),
                iam.ServicePrincipal("s3.amazonaws.com")
            )
        )
        self._service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeCommitPowerUser'))
        self._service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess'))
        self._service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'))

        self._service_role.apply_removal_policy(RemovalPolicy.DESTROY)

        # Create SageMaker instance
        self._notebook_lifecycle = sagemaker.CfnNotebookInstanceLifecycleConfig(
            self, f'{self._PREFIX}-LifeCycleConfig-east-1',
            notebook_instance_lifecycle_config_name='ae-config',
            on_create=[sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty(
                content=Fn.base64(f"""
                    #!/bin/bash
                    set -ex

                    BUCKET="{bucket_name}"
                    PREFIX="sagemaker"
                    DIRECTORY="ae_detection"

                    cd home/ec2-user/SageMaker && mkdir -p $DIRECTORY
                    aws s3 cp s3://$BUCKET/$PREFIX /home/ec2-user/SageMaker/$DIRECTORY --recursive
                    sudo chown "ec2-user":"ec2-user" /home/ec2-user/SageMaker/$DIRECTORY --recursive
                """)
            )]
        )
         # Add removal policy for the lifecycle configuration
        self._notebook_lifecycle.apply_removal_policy(RemovalPolicy.DESTROY)

        self.notebook = sagemaker.CfnNotebookInstance(
            self, f'{self._PREFIX}-notebook',
            role_arn=self._service_role.role_arn,
            instance_type='ml.t2.medium',
            root_access="Enabled",
            notebook_instance_name='AdverseEventDetectionModeling',
            lifecycle_config_name ='ae-config'
        )
        # Add removal policy for the notebook instance
        self.notebook.apply_removal_policy(RemovalPolicy.DESTROY)