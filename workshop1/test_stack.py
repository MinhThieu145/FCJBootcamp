from aws_cdk import (
    # Duration,
    Stack,

    # aws batch
    aws_batch as batch,

    # iam
    aws_iam as iam,
)
from constructs import Construct

# import the child stack
from workshop1.cicd_stack import CICDStack

from workshop1.run_task_stack import RunTaskStack

# some libs
import os

# load the environment variables
from dotenv import load_dotenv
load_dotenv()

# load
ECR_REPO_NAME = os.getenv("ECR_REPO")
JOB_DEFINITION_NAME = os.getenv("JOB_DEFINITION")
JOB_QUEUE_NAME = os.getenv("JOB_QUEUE")
JOB_NAME = os.getenv("JOB_NAME")
BATCH_ROLE = os.getenv("BATCH_ROLE")



class TestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # For the simplicity of this, let create a role for Batch. Can be modified for more policies
        batch_role = iam.Role(
            scope=self,
            id=f"{BATCH_ROLE}",
            role_name=f"{BATCH_ROLE}",
            assumed_by=iam.ServicePrincipal("batch.amazonaws.com"),

            # add the full S3 access to the role
            managed_policies=[
                # add the BatchServiceRolePolicy to the role
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    managed_policy_name="service-role/AWSBatchServiceRole"
                ),

            ],
        )


         # create compute environment
        compute_environment = batch.CfnComputeEnvironment(
            scope=self,
            id="JobScrapingComputeEnvironment",
            compute_environment_name='job-scraping-compute-environment',
            
            # if you set the type as MANAGED, it will pass in the the settings from Launch Template, otherwise you need to set the settings manually
            type='MANAGED',
            state='ENABLED',

            # Compute Resources: to set the type of compute resource
            compute_resources=batch.CfnComputeEnvironment.ComputeResourcesProperty(
                # The CPU stuff
                maxv_cpus=4,
                subnets=['subnet-044727a34c05bb730'],
                type='FARGATE_SPOT',

                # Security Group
                security_group_ids=['sg-0d2f0b2a6d2ff7c5e'],
            ),



        )
