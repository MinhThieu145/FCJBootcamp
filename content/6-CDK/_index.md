---
title : "Building a workshop with CDK"
date :  "`r Sys.Date()`" 
weight : 6
chapter : false
pre : " <b> 6. </b> "
---

## General Introduction
This is the bonus part of this workshop. You will be instructed to rebuild this workshop with CDK. 

{{% notice note%}}
*CDK at a glance: * This is an AWS service that allows building and deploying AWS resources using code. CDK supports many languages such as Python, Javascript, Typescript, Java, C#,... In this workshop, I will use CDK with Python. CDK creates stacks in Cloudformation for resource deployment. So if you get an error or need monitoring, you can go to AWS Cloudformation.
{{% /notice%}}

## Preparedness 
1. First, you need to clone github repo containing CDK code. You can use the following command:
```bash
git clone -b cdk https://github.com/MinhThieu145/FCJBootcamp.git 
```
2. After that, you need to set up the AWS CLI to interact with the resource. If you use pip, you can use the following command to install the AWS CLI: `pip install awscli`. To check, you can use the command: `aws --version`
3. After that, you need to sign in to your AWS account. You can use the following command: `aws configure`. This command will ask you to enter the Access Key and Secret Key. You can get these two keys in the IAM section of the AWS Console.
4. Go to AWS IAM, select User and select Add User
5. Go to User Name -> Next
6. In the Permission tab, select Attach policies directly -> Find and select AdministratorAccess -> Next
7. Select Create User

8. Go to IAM -> User and select the user you just created. Select the Security Credential tab.
![](/images/2023-07-20-01-34-39.png)
9. Scroll down to the Access Key section and select Create Access Key
10. Select “Use case” to Command Line Interface (CLI) -> Tick confirmation -> Next
11. Select Create Access Key
12. Next to the “Done” button, select Download .csv. This file will contain your Access Key and Secret Key. You can also copy the Access Key and the Secret Access Key directly from the console.
![](/images/2023-07-20-01-38-41.png)

13. Go back to your IDE, open the terminal and run the command `aws configure`. If CLI is installed, there will be a prompt asking for the access key and the Secret access key. Paste in and done. You can also choose the right region for the region you are using
![](/images/2023-07-20-01-41-14.png)

14. So you're done importing into your AWS account. Now you can run CDK all right now.   
