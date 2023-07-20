from aws_cdk import (
    # Duration,
    Stack,

    # aws codebuild
    aws_codebuild as codebuild,
    
    # aws iam
    aws_iam as iam,
)
from constructs import Construct

# Some pther lib
import os


# load the data for the CodeBuild from environment variables
from dotenv import load_dotenv
load_dotenv()

GITHUB_OWNER = os.getenv("OWNER")
GITHUB_REPO = os.getenv("REPO")
GITHUB_BRANCH = os.getenv("BRANCH")

# please use this line to add credential to the CodeBuild
# aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <token_value>
# The personal Token need to have enough permission to access the repo

class CICDStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the CodeBuild Project

        # Create Github Source
        github_source = codebuild.Source.git_hub(
            owner=f"{GITHUB_OWNER}",
            repo=f"{GITHUB_REPO}",
            webhook=True,
            branch_or_ref=f"{GITHUB_BRANCH}",

            # there are an option called webhook_filters: that is for the Webhook Event Filter on AWS. Leave it as default
        )

        # Create the role for the CodeBuild Project
        codebuild_role = iam.Role(
            scope=self,
            id="JobScrapingCICDRole",
            role_name="JobScrapingCICDRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),

            # add the full S3 access to the role
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    managed_policy_name="AmazonS3FullAccess"
                ),

                # add the full ECR access to the role
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    managed_policy_name="AmazonEC2ContainerRegistryFullAccess"
                ),

            ]

        )

        # Create the CodeBuild Project
        codebuild.Project(
            scope=self,
            id="CICDProject",
            project_name="CICDProject",

            # add description 
            description="CodeBuild Project for the CICD for Job Scraping Project",

            # set the source
            source=github_source,

            # add some environment variables
            environment=codebuild.BuildEnvironment(
                # add the Base Environment Variable
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,

                # set the priviledge to true for docker build
                privileged=True,                
            ),

            # Create role for the CodeBuild Project
            role=codebuild_role,
        )
