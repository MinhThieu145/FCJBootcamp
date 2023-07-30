---
title : "Thiết kế CI/CD Pipeline"
date :  "`r Sys.Date()`" 
weight : 2
chapter : false
pre : " <b> 6.1. </b> "
---

Trong phần lab trước, bạn đã học cách tạo pipeline cho crawler với Codebuild. Trong phần này, mình sẽ sử dụng CDK để thực hiện điều tương tự. Trong repo mà bạn clone về, trong folder **workshop1** có 1 file python là: **cicd_stack.py**. Đây là file setup CI/CD pipeline cho crawler. Mình sẽ đi qua từng phần trong file này. Đầu tiên là tổng quan file:
```python
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

```

## Chuẩn bị các biến môi trường cho Codebuild.
Thay vì connect trực tiếp vào Github như khi sử dụng console, bạn buộc phải sử dụng environment variable để truyền thông tin vào Codebuild. Mình sẽ sử dụng thư viện **dotenv** để load các biến môi trường từ file **.env**, nhưng bạn có thể để trong code. 

```python
# load the data for the CodeBuild from environment variables
from dotenv import load_dotenv
load_dotenv()

GITHUB_OWNER = os.getenv("OWNER")
GITHUB_REPO = os.getenv("REPO")
GITHUB_BRANCH = os.getenv("BRANCH")

```

Bên cạnh đó, mình cũng import các thư viện cần thiết cho stack
```python
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


```

Còn một bước rất quan trọng để bạn chạy được Gitbuild, đó là cấp quyền access Github cho AWS. Bạn cần lấy personal access key từ Github và sử dụng lệnh sau.
```bash
aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <token_value>
```

{{% notice warning %}}
Khi tạo personal access từ Github, bạn cần cấp đủ quyền cho AWS. Nếu bị lỗi thì cần kiểm tra lại quyền của token
{{% /notice %}}

## Tạo Github Source
Ở phần console thì bạn chọn Source từ console như trong ảnh:
![](/images/2023-07-20-02-08-52.png)

Nhưng trong CDK, bạn cần tạo Github Source bằng code. Bạn có thể tham khảo thêm tại [Github Source](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codebuild/Source.html#aws_cdk.aws_codebuild.Source.git_hub).

```python
# Create Github Source
github_source = codebuild.Source.git_hub(
    owner=f"{GITHUB_OWNER}",
    repo=f"{GITHUB_REPO}",
    webhook=True,
    branch_or_ref=f"{GITHUB_BRANCH}",

    # there are an option called webhook_filters: that is for the Webhook Event Filter on AWS. Leave it as default
)
```
## Tạo Environment
Trong console, ở tab Environment, bạn cần

- Chọn Operating System (mình dùng Ubuntu)
- tick priviledge để cho phép docker build
- Tạo 1 role mới hay chọn role có sẵn

![](/images/2023-07-20-02-12-58.png)

Trong CDK, để tạo 1 role mới 
```python
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
```
Sau đó, bạn có thể tạo Codebuild Project. Các phần như operating system, tick priviledge đều có thể làm ở đây. Bạn có thể thấy trong đoạn code bên dưới, mình đã đặt tên, description, gán source là github, tạo environment là Linux Standard 7.0 giống với console, tick priviledge và chọn role là role vừa tạo.

```python
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

```

Vậy là bạn đã hoàn tất công đoạn CI/CD