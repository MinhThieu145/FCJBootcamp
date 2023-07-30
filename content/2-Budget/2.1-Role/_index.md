---
title : "AWS Batch Design"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 2.1 </b> "
---

In this step, we will set up a complete AWS Batch to run the job. To use AWS Batch, you need to create the components that you mentioned in the previous article:
- Compute Environments
- Job Queues
- Job Definitions

## Batch Wizard 
For convenience, it is recommended to use the wizard instead of creating individual components. Go to AWS Batch and select Wizard. If you want more options, you can use EC2, or EKS if you use Kubernete. But for convenience, I'll use Fargate. 
![](/images/2023-07-09-16-30-24.png)

## Compute Environment
1. Select a name for compute env
![](/images/2023-07-09-16-33-46.png)

2. Spot Instances can help save costs, but tasks running on spot instances can be interrupted in the middle, only if the task is short or can be replaced by other jobs. I will choose not in this post. Also select the maximum vCPU, it is possible to leave 4 vCPUs.
![](/images/2023-07-09-16-36-32.png)

3. Go to the Network Configuration step, you can set up as follows
- Create a **VPC with a **public subnet**
- Remember to create an Internet Gateway and Route table for Subnet to access the internet
- Create a **security group** for compute env, open outbound traffic to the internet (default is open so no need to fix)
- Add created sections to compute env
![](/images/2023-07-09-16-43-52.png)

4. Select next to create a compute env

## Job Queue
1. Choose a name for the job queue
2. Set **Priority to 1. This is the priority order, in case you have multiple job queues in the same compute env, the high priority job queue will be run first.
![](/images/2023-07-09-16-46-28.png)

## Job Definition
1. Select the name and timeout for the job definition. Timeout** is the maximum running time of a job. If the job runs beyond this time, it will stop. I estimate my job takes less than 15 minutes, so I leave it 15 minutes (900s).
![](/images/2023-07-09-16-48-18.png)

2. Fargate, you leave **version as LATEST, turn on Public IP because the job needs access to the Internet. **Ephemeral storage** is the capacity of Fargate, to range from 21GB to 200GB. Execution roles to give your task access to the ECR to pull images from there, read Secret from Secret Manager and some low-level roles.
![](/images/2023-07-09-16-52-35.png)

3. In the container configuration, in the image section, you need to go to ECR, copy the URI of the ECR repo that you created earlier
![](/images/2023-07-09-17-05-30.png)
Paste into the Image section of the Batch Wizard and add latest to the back** so you can get the latest image 
![](/images/2023-07-09-17-08-53.png)

4. The next part is command. You can add commands to your Docker Image. This command will **not overwrite CMD or ENTRYPOINT in your docker, but will add. Because I don't need anything else, I'll leave it default, the default command just to print Hello World
![](/images/2023-07-09-17-15-14.png)

5. It seems odd to have two roles in the job definition section, however, follow [explanation] (https://repost.aws/questions/QU73a6ZU6RQg-CNJ-25i_i_Q/which-role-do-i-have-to-use-for-the-fargate-tasks-on-aws-batch) here. If your task needs higher level permissions such as S3 access (permissions that not all tasks need), you can leave it in **job role**, while lower permissions such as pull image from ECR can be fixed in **execution role. Your task needs access to S3 so it will create a Full Access S3 role, but if you don't need anything but run the task, you can go blank (select None). At the same time you need to select vCPU and Memory
![](/images/2023-07-09-17-25-46.png)

6. Choose a name for your job. When running, this name will be displayed.
![](/images/2023-07-09-17-29-22.png)

7. Once you're done, select Review and Create Resource. So you have completed the AWS Batch setup. To check, you can go to Job Definition and select Submit New Job

