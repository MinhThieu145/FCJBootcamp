from aws_cdk import (
    # Duration,
    Stack,
    # iam
    aws_iam as iam,

    # aws batch
    aws_batch as batch,

    # lambda
    aws_lambda as aws_lambda,

    # Duration
    Duration,

    # aws events
    aws_events as events, 

    # aws events targets
    aws_events_targets as targets,

    # aws ec2 (for vpc)
    aws_ec2 as ec2,

)
from constructs import Construct

# Other lib
import os

# load the environment variables
from dotenv import load_dotenv
load_dotenv()

# load
ECR_REPO_NAME = os.getenv("ECR_REPO")
JOB_DEFINITION_NAME = os.getenv("JOB_DEFINITION")
JOB_QUEUE_NAME = os.getenv("JOB_QUEUE")
JOB_NAME = os.getenv("JOB_NAME")
JOB_ROLE_NAME = os.getenv("ECS_ROLE_NAME")
BATCH_VPC_NAME = os.getenv("BATCH_VPC_NAME")
BATCH_SUBNET_NAME = os.getenv("BATCH_SUBNET_NAME")
BATCH_SG_NAME = os.getenv("BATCH_SG_NAME")


class RunTaskStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # aws batch
        
        # For the simplicity of this, let create a role for ECS job
        ecs_role = iam.Role(
            scope=self,
            id=f"{JOB_ROLE_NAME}",
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
            role_name=f'{JOB_ROLE_NAME}',
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonECSTaskExecutionRolePolicy'),

                # add full access to S3
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),

                # add full access to ECR
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ContainerRegistryFullAccess'),
            ],
        )
        
        # +++ Create a VPC for the Batch +++
        vpc = ec2.Vpc(
            scope=self,
            id = f"{BATCH_VPC_NAME}",
            vpc_name=f"{BATCH_VPC_NAME}",

            # set the max azs to 1
            max_azs=1,

            # set the cidr
            cidr='10.0.0.0/16',

            # set the subnet configuration
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{BATCH_SUBNET_NAME}",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
            ],

        )

        # Create a Security Group for the Batch in the VPC
        batch_security_group = ec2.SecurityGroup(
            scope=self,
            id=f"BatchSecurityGroup",
            vpc=vpc,
            security_group_name=f"{BATCH_SG_NAME}",

            # allow all outbound traffic
            allow_all_outbound=True,

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
                maxv_cpus=4,
                subnets=[vpc.public_subnets[0].subnet_id],
                type='FARGATE_SPOT',

                # Security Group
                security_group_ids=[batch_security_group.security_group_id],
            ),

            # Service Role Not neccessary
            # service_role=batch_role.role_arn,
            
        )

        # create job queue
        job_queue = batch.CfnJobQueue(
            scope=self,
            id=f"{JOB_QUEUE_NAME}",
            job_queue_name=f'{JOB_QUEUE_NAME}',
            priority=1,
            state='ENABLED',
            compute_environment_order=[
                batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment=compute_environment.ref,
                    order=1,
                )
            ],
        )

        # create job definition
        job_definition = batch.CfnJobDefinition(
            scope=self,
            id=f"{JOB_DEFINITION_NAME}",
            job_definition_name=f'{JOB_DEFINITION_NAME}',

            timeout={
                'attemptDurationSeconds': 900,
            },

            # type (so this is not multi-node)
            type='container',

            platform_capabilities=['FARGATE'],

            # container properties
            container_properties=batch.CfnJobDefinition.ContainerPropertiesProperty(
                

                # THIS IS "SOME" OF THE FARGATE PLATFORM CONFIGURATION. THE REASON I SAID SOME IS BECAUSE, NOT SURE WHY, THE SETTINGS ARE IN MANY PLACES

                # assign public IP (does not found)
                
                # Ephemeral storage
                ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                    size_in_gib=30 # between 21 and 200
                ), 

                # Execution role
                execution_role_arn=ecs_role.role_arn,

                # ++++ THIS IS SOME MORE FARGATE CONFIGURATION +++++

                # This is the Latest that you see in the console
                fargate_platform_configuration= batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                    platform_version='LATEST',

                ),

                # network configuration (For public IP)
                network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                    assign_public_ip='ENABLED',
                ),

                # privileged: Do not add this!!! Fargate actually ban this
                # privileged=True,
                

                # THIS IS ON THE TAB CONTAINER CONFIGURATION IN JOB DEFINITION (Step 2 if you use Console)

                # This is the link to the ECR that we store our image (the image that we build, and create in the CICD step). Don't forget to add the tag
                image=f'{ECR_REPO_NAME}:latest',

                # Honestly, this is not really useful, since I have already set the ENTRYPOINT in the Dockerfile
                command=[
                    'echo',
                    'Job Definition Initiated',
                ],

                # job role: Explain simply, Job role is more specific than Execution role. All the job can have the same execution role, but different job role
                job_role_arn=ecs_role.role_arn,

                # memory and vcpus
                resource_requirements=[
                    batch.CfnJobDefinition.ResourceRequirementProperty(
                        type='MEMORY',
                        value='2048',
                    ),

                    batch.CfnJobDefinition.ResourceRequirementProperty(
                        type='VCPU',
                        value='1',
                    ),

                ],

            ),

        )   

        # +++ Create a Lambda to submit job to Batch +++

        # create a role for lambda to submit job to batch
        submit_job_lambda_role = iam.Role(
            scope=self,
            id="SubmitBatchJobLambdaRole",
            role_name="SubmitJobLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),

            # add the job submit policy to the role
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    managed_policy_name="service-role/AWSBatchServiceEventTargetRole"
                ),
            ],

        )
        # create a lambda function
        submit_job_lambda = aws_lambda.Function(
            scope=self,
            id="SubmitJobLambda",
            function_name="CDK-JobScraping-Submit-Job-Batch",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset("workshop1/lambda_functions/TriggerJobScrapingTask/"),
            handler="lambda_function.lambda_handler",
            timeout=Duration.seconds(60),

            # pass in the role
            role=submit_job_lambda_role,

            environment={
                "JOB_NAME": JOB_NAME,
                "JOB_QUEUE": JOB_QUEUE_NAME,
                "JOB_DEFINITION": JOB_DEFINITION_NAME,
            },
        )

        # +++ Event Bridge Rule +++
        # create a rule to trigger the lambda function at 6am everyday
        rule = events.Rule(
            scope=self,
            id="TriggerSubmitJobLambda",
            rule_name="TriggerSubmitJobLambda",
            schedule=events.Schedule.cron(
                minute="0",
                hour="6",
            ),
        )

        # add the lambda function as the target
        rule.add_target(targets.LambdaFunction(submit_job_lambda))





    





                

