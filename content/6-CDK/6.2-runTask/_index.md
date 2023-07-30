---
title : "AWS Batch Design"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 6.2. </b> "
---

In the previous section, after I finished designing the CI/CD pipeline, I continued with AWS Batch. In this section, I'll go through each step of designing AWS Batch using CDK, including

- Create a role for the batch. In the AWS Batch Console, there is a framework called Execution Role. I need to create and assign this role to the batch.
- Design VPC network infrastructure for Batch 
- Create Security Group for Batch
- Create remaining components for Batch: Compute Env, Job Definition, Job Queue, etc.
- Create EventBridge to be able to Schedule the Batch to run on a schedule

If you wonder why there is no bucket. In this workshop, I created a manual bucket. The reason is that passing bucket name into script crawler is quite difficult due to the way I write the script. Therefore, I will have to create a bucket, pass the bucket name into the crawler script, and then be able to run the crawler.

```python
from ws_cdk import (
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
load_dotenv ()

# load
ECR_REPO_NAME = os.getenv (“ECR_REPO”)
JOB_DEFINITION_NAME = os.getenv (“JOB_DEFINITION”)
JOB_QUEEUE_NAME = os.getenv (“JOB_QUEUE”)
JOB_NAME = os.getenv (“JOB_NAME”)
JOB_ROLE_NAME = os.getenv (“ECS_ROLE_NAME”)
BATCH_VPC_NAME = os.getenv (“BATCH_VPC_NAME”)
BATCH_SUBNET_NAME = os.getenv (“BATCH_SUBNET_NAME”)
BATCH_SG_NAME = os.getenv (“BATCH_SG_NAME”)


RunTaskStack class (Stack):

def __init__ (self, scope: Construct, construct_id: str, **kwargs) -> None:
super () .__init__ (scope, construct_id, **kwargs)

# aws batch
        
# For the simplicity of this, let's create a role for ECS job
ecs_role = iam.role (
scope=self,
id=f "{JOB_ROLE_NAME}”,
assumed_by=iam.servicePrincipal ('ecs-tasks.amazonaws.com'),
role_name=f' {JOB_ROLE_NAME} ',
managed_policies= [
IAM.MANAGEDPOLICY.FROM_AWS_MANAGED_POLICY_NAME ('SERVICE-ROLE/AMAZONECSTASKExecutionRolePolicy'),

# add full access to S3
IAM.MANAGEDPOLICY.FROM_AWS_MANAGED_POLICY_NAME ('AMAZONS3FULLACCESS'),

# add full access to ECR
IAM.managedpolicy.from_aws_managed_policy_name ('Amazonec2ContainerRegistryFullAccess'),
],
)
        
# +++ Create a VPC for the Batch +++
vpc = ec2. Vpc (
scope=self,
id = f "{BATCH_VPC_NAME}”,
vpc_name=f "{BATCH_VPC_NAME}”,

# set the max azs to 1
max_azs=1,

# set the cidr
cidr='10.0.0.0/16',

# set the subnet configuration
subnet_configuration= [
ec2. SubNetConfiguration (
name=f "{BATCH_SUBNET_NAME}”,
subnet_type=ec2. Subnettype.public,
cidr_mask=24,
),
],

)

# Create a Security Group for the Batch in the VPC
batch_security_group=ec2. SecurityGroup (
scope=self,
id=f"BatchSecurityGroup”,
vpc=vpc,
security_group_name=f "{BATCH_SG_NAME}”,

# allow all outbound traffic
allow_all_outbound=True,

)

# create compute environment
compute_environment = batch.cfnComputeenVironment (
scope=self,
id="JobScrapingComputeenVironment”,
compute_environment_name='job-scraping-compute-environment',
            
# if you set the type as MANAGED, it will pass in the settings from Launch Template, otherwise you need to set the settings manually
type='managed',
state='Enabled',

# Compute Resources: to set the type of compute resource
compute_resources=batch.cfnComputeenVironment.ComputeresSourcesProperty (
maxv_cpus=4,
subnets= [vpc.public_subnets [0] .subnet_id],
type='Fargate_Spot',

# Security Group
security_group_ids= [batch_security_group.security_group_id],
),

# Service Role Not Necessary
# service_role=batch_role.role_arn,
            
)

# create a job queue
job_queue = batch.cfnJobQueue (
scope=self,
id=f "{JOB_QUEUE_NAME}”,
job_queue_name=f' {JOB_QUEUE_NAME} ',
priority=1,
state='Enabled',
compute_environment_order= [
Batch.cfnJobQueue.computeenVironmentorderProperty (
compute_environment=compute_environment.ref,
order=1,
)
],
)

# create job definition
job_definition = batch.cfnjobDefinition (
scope=self,
id=f "{JOB_DEFINITION_NAME}”,
job_definition_name=f' {JOB_DEFINITION_NAME} ',

timeout= {
'AttemptDurationSeconds': 900,
},

# type (so this is not multi-node)
type='container',

platform_capabilities= ['FARGATE'],

# container properties
container_properties=Batch.cfnjobDefinition.ContainerPropertiesProperty (
                

# THIS IS “SOME” OF THE FARGATE PLATFORM CONFIGURATION. THE REASON I SAID SOME IS BECAUSE, NOT SURE WHY, THE SETTINGS ARE IN MANY PLACES

# assign public IP (does not found)
                
# Ephemeral storage
epheemeral_storage=Batch.cfnjobdefinition.ephemeralstorageProperty (
size_in_gib=30 # between 21 and 200
), 

# Execution role
execution_role_arn=ecs_role.role_arn,

# ++++ THIS IS SOME MORE FARGATE CONFIGURATION +++++

# This is the latest that you see in the console
fargate_platform_configuration= batch.cfnjobdefinition.fargateplatformconfigurationProperty (
platform_version='latest',

),

# network configuration (For public IP)
Network_Configuration=Batch.cfnJobDefinition.NetworkConfigurationProperty (
assign_public_ip='Enabled',
),

# privileged: Do not add this!!! Fargate actually ban this
# privileged=True,
                

# THIS IS ON THE TAB CONTAINER CONFIGURATION IN JOB DEFINITION (Step 2 if you use Console)

# This is the link to the ECR that we store our image (the image that we build, and create in the CICD step). Don't forget to add the tag
image=f' {ECR_REPO_NAME} :latest',

# Honestly, this is not really useful, since I have already set the ENTRYPOINT in the Dockerfile
command= [
'echo',
'Job Definition Initiated',
],

# job role: Explain simply, job role is more specific than Execution role. All the jobs can have the same execution role, but different job roles
job_role_arn=ecs_role.role_arn,

# memory and vcpus
resource_requirements= [
Batch.cfnjobDefinition.ResourceEquirementProperty (
type='Memory',
value='2048',
),

Batch.cfnjobDefinition.ResourceEquirementProperty (
type='vcpu',
value='1',
),

],

),

)   

# +++ Create a Lambda to submit job to Batch +++

# create a role for lambda to submit job to batch
submit_job_lambda_role = iam.role (
scope=self,
id="SubmitBatchJobLambDarole”,
role_name="SubmitJobLambDarole”,
Assumed_by=Iam.servicePrincipal (“lambda.amazonaws.com”),

# add the job submit policy to the role
managed_policies= [
IAM.ManagedPolicy.From_AWS_Managed_Policy_Name (
managed_policy_name="Service-role/AWSBatchServiceEventTargetRole”
),
],

)
# create a lambda function
submit_job_lambda = AWS_Lambda.function (
scope=self,
id="SubmitJobLambda”,
function_name="cdk-jobscraping-submit-job-batch”,
runtime=AWS_lambda.runtime.python_3_9,
code=AWS_Lambda.code.from_asset (“Workshop1/Lambda_Functions/TriggerjobScrapingTask/”),
handler="lambda_function.lambda_handler”,
timeout=Duration.seconds (60),

# pass in the role
role=submit_job_lambda_role,

environment= {
“JOB_NAME”: JOB_NAME,
“JOB_QUEUE”: JOB_QUEUE,
“JOB_DEFINITION”: JOB_DEFINITION_NAME,
},
)

# +++ Event Bridge Rule +++
# create a rule to trigger the lambda function at 6am everyday
rule = events.rule (
scope=self,
id="TriggerSubmitJobLambda”,
rule_name="TriggerSubmitJobLambda”,
schedule=events.schedule.cron (
minute="0",
hour="6",
),
)

# add the lambda function as the target
rule.add_target (targets.lambdaFunction (submit_job_lambda))

```
