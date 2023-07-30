---
title : "Frontend Webapp Design"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 6.3. </b> "
---

In my opinion, this is the hardest part of all three parts when working with CDK. The reason is because this part is very long. Here's an overview of what we're going to do in this section:

## Network Infrastructure Design 
The code below creates a VPC with 2 subnets, 1 public and 1 private. When creating a public subnet with code, AWS routes itself to the Internet Gateway for itself. And when creating a Private Subnet of the type `PRIVATE_WITH_NAT`, AWS creates its own NAT Gateway. 

```python
# Create VPC
vpc = ec2. Vpc (
scope=self,
id='CdkJobScrapingFrontEnd',
vpc_name=f' {VPC_NAME} ',

# set the CIDR for the VPC
cidr= '10.0.0.0/16',

# enable DNS support
enable_dns_support=True,

# setup 2 subnet
subnet_configuration= [

# public subnet
ec2. SubNetConfiguration (
name="CDKjobScrapingFrontendPublic”,
subnet_type=ec2. Subnettype.public,
cidr_mask=24,
),

# private subnet with NAT
ec2. SubNetConfiguration (
name="CDKjobScrapingFrontendPrivate”,
subnet_type=ec2. subnettype.private_with_nat,
cidr_mask=24,
),
],

)

```

## Creating Security Groups for EC2 Instances and Bastion Hosts
```python
# +++ Create EC2 +++

# create a security group for the ec2 private instance
private_ec2_security_group=ec2. SecurityGroup (
scope=self,
id="CDKjobScrapingFrontendSecurityGroup”,
vpc=vpc,
allow_all_outbound=True,
description="Security Group for the EC2 private instance”,
security_group_name="CDK-Jobscraping-frontend-private-SG”,
            
)

# add the rules to the security group, open custom TPC port 8501
private_ec2_security_group.add_ingress_rule (
peer=ec2. Peer.any_IPv4 (),
connection=ec2. Port.TCP (8501),
Description="Allow inbound traffic from anywhere for port 8501",
)

# add ssh port 22 for SG for the EC2 private instance
private_ec2_security_group.add_ingress_rule (
peer=ec2. Peer.any_IPv4 (),
connection=ec2. Port.TCP (22),
description="Allow inbound traffic from anywhere for port 22",
)


# create security group for bastion host
bastion_security_group=ec2. SecurityGroup (
scope=self,
id="CDKjobScrapingFrontendBastionSecurityGroup”,
vpc=vpc,
allow_all_outbound=True,
description="Security Group for the bastion host”,
security_group_name="CDK-Jobscraping-frontend-bastion-SG”,
            
)

# add the rules to the security group, open SSH port 22
bastion_security_group.add_ingress_rule (
peer=ec2. Peer.any_IPv4 (),
connection=ec2. Port.TCP (22),
description="Allow inbound traffic from anywhere for port 22",
)

```

## Creating a Bastion Host
Note: Since I can't find a way to download the pem key when using CDK, you will have to create a pem key and save the name in the environment variable.
```python
# create a bastion host

# AMI for bastion host
ami_bastion_host = ec2. Machineimage.generic_Linux (
{
“us-east-1":" ami-053b0d53c279acc90"
}
)

# DON'T FORGET THAT YOU WILL NEED TO CREATE A KEY PAIR IN THE AWS CONSOLE (BECAUSE YOU COULDN'T ACCESS IT LATTER IF CREATE HERE)
bastion_host = ec2. Instance (
scope=self,
id="CDKjobScrapingFrontendBastionHost”,
instance_type=ec2. InstanceType (“t2.micro”),
machine_image=ec2. MachineImage.Latest_Amazon_Linux (
generation=ec2. AmazonLinuxGeneration.Amazon_Linux_2
),
vpc=vpc,
vpc_subnets=ec2. SubnetSelection (
subnet_type=ec2. Subnettype.public
),
security_group=bastion_security_group,
key_name=f' {KEY_NAME} ',
instance_name='cdkjobscrapingfrontendbastionhost',
)

```

## Create ASG and ALB

In the code below, I have:
  
- Create a role for ASG
- Create a Launch Instance. You need to assign a pem key if you want to access the instance later. Launch instances also need SG. Also, you need to assign user data to the launch template.
- Create ASG
- Generate ALP
- Create Target Group and assign ASG to Target Group

```python

# +++ Create Load Balancer and Auto Scaling Group +++

# But first, we will need 2 things
#1. Create an AMI that has all the packages installed
#3. Create a Role for ASG

# Since the first steps would be done in console, I'll do the 3rd step here
        
# Create a role for ASG
Role = iam.Role (
scope=self,
id='cdkJobScrapingFrontEndrole',
asumed_by=iam.servicePrincipal ('ec2.amazonaws.com'),
role_name='cdkjobscrapingfrontendrole',
managed_policies= [
# Read access to EC2
IAM.ManagedPolicy.From_AWS_Managed_Policy_Name ('Amazonec2ReadOnlyAccess'),

# Full access to S3
IAM.MANAGEDPOLICY.FROM_AWS_MANAGED_POLICY_NAME ('AMAZONS3FULLACCESS'),

]]
)


# Okay, now let's move on to create the Load Balancer and Auto Scaling Group


# Create Launch Template. Don't Forget a Key Pair
launch_template=ec2. LaunchTemplate (
scope=self,
id='CdkJobScrapingFrontEndLaunchTemplate',
launch_template_name='cdkjobscrapingfrontendLaunchtemplate',        

# set the machine image from the AMI that we created
machine_image=ec2. Machineimage.generic_Linux (
{
“us-east-1":f' {AMI} '
}
),

# set the instance type
instance_type=ec2. InstanceType (“t2.micro”),

# set the key pair
key_name=f' {KEY_NAME} ',

# set the security group
security_group=private_ec2_security_group,

# set the role
role=role,

# set the block device mapping: use AMI block device mapping
user_data=ec2. UserData.custom (         
“'Content-Type: multipart/mixed; boundary=”//”
Mime-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii”
Mime-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename=” cloud-config.txt”

#cloud -config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii”
Mime-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename=” userdata.txt”

#! /bin/bash

# Run the app.py script
cd /home/ubuntu/

sudo streamlit run streamlit-app.py > output.txt 2>&1

--//--"'
),
)


# Create Auto Scaling Group
auto_scaling_group = autoscaling.autoscalingGroup (
scope=self,
vpc=vpc,
id='CdkJobScrapingFrontEndAutoScalingGroup',

                        

# set the name for the Auto Scaling Group
auto_scaling_group_name='cdkjobscrapingfrontendautoscalinggroup',

# set launch template
launch_template = launch_template,
                
# VPC private subnet
vpc_subnets=ec2. SubnetSelection (
subnet_type=ec2. SubnetType.Private_With_NAT # current we have only 2 private sbunet, so can use this to select all
),

# set the min, max, and desired capacity
min_capacity=0,
max_capacity=2,
desired_capacity=1,

            

)
        
# create a load balancer
load_balancer = elbv2. ApplicationLoadBalancer (
scope=self,
id='CdkJobScrapingFrontEndLoadBalancer',
vpc=vpc,
Internet_facing=True,
load_balancer_name='cdkjobscrapingfrontendlb',
security_group=private_ec2_security_group,
)

# create a target group that targets to the Auto Scaling Group

target_group=elbv2. ApplicationTargetGroup (
scope=self,
id='CdkJobScrapingFrontEndTargetGroup',
vpc=vpc,
port=8501,
protocol=elbv2. ApplicationProtocol.http,
targets= [auto_scaling_group],
target_group_name='cdkjobscrapingfrontendtg',
)    

            
# create a listener that listeners to the target group
listener = load_balancer.add_listener (
id='cdkJobScrapingFrontendListEner',
port=8501,
protocol=elbv2. ApplicationProtocol.http,
open=True,
default_target_groups= [target_group],
)

```
