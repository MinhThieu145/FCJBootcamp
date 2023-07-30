---
title : "CI/CD Pipeline Design"
date :  "`r Sys.Date()`" 
weight : 2
chapter : false
pre : " <b> 6.1. </b> "
---

In the previous lab, you learned how to create crawler pipelines with Codebuild. In this section, I will use CDK to do the same. In the repo that you clone, in the folder **workshop1** there is a python file: **cicd_stack.py**. This is the CI/CD pipeline setup file for crawler. I'll go through each section of this file. The first is an overview of the file:
```python
from ws_cdk import (
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
load_dotenv ()

GITHUB_OWNER = os.getenv (“OWNER”)
GITHUB_REPO = os.getenv (“REPO”)
GITHUB_BRANCH = os.getenv (“BRANCH”)

# please use this line to add credential to the CodeBuild
# aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <token_value>
# The personal token needs to have enough permission to access the repo

cicdStack class (Stack):

def __init__ (self, scope: Construct, construct_id: str, **kwargs) -> None:
super () .__init__ (scope, construct_id, **kwargs)

# Create the CodeBuild Project

# Create Github Source
github_source = codebuild.source.git_hub (
owner=f "{GITHUB_OWNER}”,
repo=f "{GITHUB_REPO}”,
webhook=True,
branch_or_ref=f "{GITHUB_BRANCH}”,

# there are an option called webhook_filters: that is for the Webhook Event Filter on AWS. Leave it as default
)

# Create the role for the CodeBuild Project
codebuild_role = iam.role (
scope=self,
id="JobScrapingCicDrole”,
Role_name="JobScrapingCicDrole”,
Assumed_by=Iam.servicePrincipal (“codebuild.amazonaws.com”),

# add the full S3 access to the role
managed_policies= [
IAM.ManagedPolicy.From_AWS_Managed_Policy_Name (
managed_policy_name="Amazons3fullAccess”
),

# add full ECR access to the role
IAM.ManagedPolicy.From_AWS_Managed_Policy_Name (
managed_policy_name="Amazonec2ContainerRegistryFullAccess”
),

]]

)

# Create the CodeBuild Project
CodeBuild.project (
scope=self,
id="cicdproject”,
project_name="cicdproject”,

# add description 
Description="CodeBuild Project for the CICD for Job Scraping Project”,

# set the source
source=github_source,

# add some environment variables
environment=CodeBuild.BuildEnvironment (
# add the Base Environment Variable
build_image=codebuild.linuxbuildimage.standard_7_0,

# set the privilege to true for docker build
privileged=True,                
),

# Create a role for the CodeBuild Project
role=codebuild_role,
)

```

## Preparation of environment variables for Codebuild.
Instead of connecting directly to Github as a console, you must use environment variable to pass information into Codebuild. I will use the **dotenv library to load the environment variables from the **.env** file, but you can leave it in the code. 

```python
# load the data for the CodeBuild from environment variables
from dotenv import load_dotenv
load_dotenv ()

GITHUB_OWNER = os.getenv (“OWNER”)
GITHUB_REPO = os.getenv (“REPO”)
GITHUB_BRANCH = os.getenv (“BRANCH”)

```

In addition, I also import the necessary libraries for the stack
```python
from ws_cdk import (
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
load_dotenv ()


```

Another very important step for you to run Gitbuild is to grant access to Github to AWS. You need to get your personal access key from Github and use the following command.
```bash
aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <token_value>
```

{{% notice warning%}}
When you create personal access from Github, you need to grant AWS permissions. If it fails, it is necessary to check the rights of the token
{{% /notice%}}

## Create Github Source
In the console, select Source from the console as shown in the image:
![](/images/2023-07-20-02-08-52.png)

But in CDK, you need to create Github Source with code. You can find out more at [Github Source] (https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codebuild/Source.html#aws_cdk.aws_codebuild.Source.git_hub).

```python
# Create Github Source
github_source = codebuild.source.git_hub (
owner=f "{GITHUB_OWNER}”,
repo=f "{GITHUB_REPO}”,
webhook=True,
branch_or_ref=f "{GITHUB_BRANCH}”,

# there are an option called webhook_filters: that is for the Webhook Event Filter on AWS. Leave it as default
)
```
## Create Environment
In the console, in the Environment tab, you need to

- Select Operating System (I use Ubuntu)
- tick privilege to allow docker build
- Create a new role or select an existing one

![](/images/2023-07-20-02-12-58.png)

In CDK, to create a new role 
```python
# Create the role for the CodeBuild Project
codebuild_role = iam.role (
scope=self,
id="JobScrapingCicDrole”,
Role_name="JobScrapingCicDrole”,
Assumed_by=Iam.servicePrincipal (“codebuild.amazonaws.com”),

# add the full S3 access to the role
managed_policies= [
IAM.ManagedPolicy.From_AWS_Managed_Policy_Name (
managed_policy_name="Amazons3fullAccess”
),

# add full ECR access to the role
IAM.ManagedPolicy.From_AWS_Managed_Policy_Name (
managed_policy_name="Amazonec2ContainerRegistryFullAccess”
),

]]

)
```
After that, you can create a Codebuild Project. Parts like operating system, tick privilege can be done here. You can see in the code below, I named it, description, assigned the source as github, created the environment as Linux Standard 7.0 similar to the console, tick privilege and choose the role as the role just created.

```python
# Create the CodeBuild Project
CodeBuild.project (
scope=self,
id="cicdproject”,
project_name="cicdproject”,

# add description 
Description="CodeBuild Project for the CICD for Job Scraping Project”,

# set the source
source=github_source,

# add some environment variables
environment=CodeBuild.BuildEnvironment (
# add the Base Environment Variable
build_image=codebuild.linuxbuildimage.standard_7_0,

# set the privilege to true for docker build
privileged=True,                
),

# Create a role for the CodeBuild Project
role=codebuild_role,
)

```

So you have completed the CI/CD.
