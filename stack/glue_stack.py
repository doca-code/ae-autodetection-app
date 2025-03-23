from aws_cdk import (
    aws_iam as iam,
    aws_glue as glue,
    RemovalPolicy,
    Stack  # Use Stack from aws_cdk now, instead of core.Construct
)

from constructs import Construct  # Import Construct from constructs

class GlueStack(Stack):  # Change to Stack instead of Construct

    def __init__(self, scope: Construct, construct_id: str, target_bucket: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._PREFIX = construct_id

        # Create Role for the Glue crawler
        self._service_role = iam.Role(
            self, f'{self._PREFIX}-ServiceRole-east-1',
            #role_name=f'{self._PREFIX}-ServiceRole',
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal('glue.amazonaws.com'),
            )
        )
        self._service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'))
        self._service_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSGlueServiceRole'))

        self._glue_crawler = glue.CfnCrawler(
            self, "InferenceResultCrawler-east-1",
            database_name="s3_tweets_db", 
            name="s3_tweets_crawler",
            role=self._service_role.role_arn,
            schedule=glue.CfnCrawler.ScheduleProperty(schedule_expression="cron(29 0/1 * * ? *)"),
            targets={"s3Targets": [{"path": f"s3://{target_bucket}/lambda_predictions/"}]}
        )
        # ✅ Apply Removal Policies to Prevent `cdk destroy` Failures
        self._glue_crawler.apply_removal_policy(RemovalPolicy.DESTROY)
        self._service_role.apply_removal_policy(RemovalPolicy.DESTROY)

