---
title : "Generate resources: ALB and ASG"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 3.2. </b> "
---

After completing the process of creating a VPC, you need to create additional resources in the VPC. In this article, we will create the following resources:

- Launch Template: This is like 1 drawing. Instace created from ASG will resemble this drawing. And to create a Launch Template with all the necessary packages, I will create an AMI

{{% notice note%}}
*Amazon Machine Image (AMI) at a glance: * AMI can be understood as a drawing of an instance. When creating a new EC2 instance, you are asked to select AMI. Most of you will use **base image**, AMIs provided by AWS such as ubuntu, linux, or window. However, if we want EC2 to be created with existing packages, we can create a custom image. 
{{% /notice%}}

- ASG: Create ASG using the Launch Template above
- ALB: Create ALB to navigate request


## Create Custom AMI and Launch Template
When instances are initialized from ASG, they need a template. To create a launch template, we first need to create a custom AMI with all the necessary packages.

1. Go to EC2, select Launch Template** and then select Create launch template**
![](/images/2023-07-09-22-27-45.png)

2. Name the template and select the option **Auto Scaling Guidance** for convenient integration with ASG later. 
![](/images/2023-07-09-22-30-02.png)

3. Select AMI and click Browse more AMIs
![](/images/2023-07-09-22-31-32.png)

4. Enter the number `238101178196` in the search bar and select **Community AMI**, you should see an AMI with the name shown below. This is my public AMI, curing the files running the server. If you follow the previous steps, especially the bucket naming of S3, you can use it without any changes. 
![](/images/2023-07-09-22-45-00.png)


{{% notice info%}}

Inside AMI, you have a streamlit server with port 8501, and save the results to S3 in Bucket named **job-description-process**, and retrieved from the folder named **indeed-scraper**

{{% /notice%}}

5. Select that AMI, and you will be taken back to the template to continue. In the “Instance Type” section, select **t2.micro**. In the Key Pair section, select a key pair that you already have so that later it is convenient to SSH into the instance (of course, through Bastion Host)
![](/images/2023-07-09-22-48-34.png)

6. The Network Settings section you can leave blank (do not select anything)
![](/images/2023-07-09-22-54-18.png)


7. You can leave the rest default.

8. In Advanced details**, expand and select Create new IAM profile, because the Frontend app needs a few roles (Access S3 and read EC2). Create a new role with the following policies
![](/images/2023-07-10-00-17-40.png)

9. Once created, go back to the template, reload (the round arrow next to it) to see the created role and select
![](/images/2023-07-10-00-19-03.png)

10. Then select Create launch template** to create the template.

## Create Auto Scaling Group

1. Go to EC2, scroll down to the last to see the ALB.
![](/images/2023-07-09-20-10-07.png)

2. Select Create Auto Scaling Group and choose a name for ASG. Then in the Launch Template** section, select the Template you created earlier, choose the version as Latest
![](/images/2023-07-19-22-49-00.png)

1. In the Network tab, select the VPC you created earlier. In that VPC, select both Private Subnet** that you created earlier. We will place the application in Private Subnet to increase security, Public Subnet only to create NAT Gateway and set Bastion Host. Click Next
![](/images/2023-07-09-23-14-06.png) 

1. In the Load Balancing tab, select Attach to new load balancer. In the newly opened tab, select Application Load Balancer, select a name for Load Balancer, and select **Internet-facing
![](/images/2023-07-09-23-21-12.png)  

1. Next is the network mapping section, the VPC will remain the same as that of ASG (of course, ELB to handle traffic into ASG, so it needs to be the same VPC). You need to select 2 Public Subnet** to set the ELB
![](/images/2023-07-09-23-25-46.png)

1. In the Listener and Routing section, select **Port as **8501** for Streamlit, and select Create a target group** and name the target group
![](/images/2023-07-09-23-29-21.png)

1. In the Health checks section, select Turn on Elastic Load Balancing Health Checks. Also set the Health Check Grace Period to 300s. This is the estimated time it takes for EC2 to start (this is a way for the EC2 instance to avoid being destroyed when it is not finished booting. If User Data causes the instance to take startup time, estimate the time it takes to boot here).
![](/images/2023-07-09-23-54-26.png)

1. Leave the Additional settings** section as default and click Next

2. Groupsize consists of three parts: **Maximum capacitance for maximum instance, **Minimum capacity is the minimum number of instances, **Desired capacity is the number of instances that ASG tries to hold at that level.
![](/images/2023-07-10-00-01-22.png)

1. Leave the Scaling Policies section blank and select Next

2. Skip the Add Notifications** section and select Next. Skip tags and next and select Create Auto Scaling Group

