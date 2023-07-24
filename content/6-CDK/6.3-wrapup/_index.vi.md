---
title : "Thiết kế frontend Webapp"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 6.3. </b> "
---

Theo mình thì đây là phần khó nhất trong cả 3 phần khi làm bằng CDK. Lý do là vì phần này rất dài. Sau đây là tổng quan về những gì mình sẽ làm trong phần này:

## Thiết kế hạ tầng mạng 
Đoạn code dưới tạo 1 VPC với 2 subnet, 1 public và 1 private. Khi tạo Public Subnet bằng code thì AWS tự route tới Internet Gateway cho mình. Và khi tạo Private Subnet loại `PRIVATE_WITH_NAT` thì AWS tự tạo NAT Gateway cho mình. 

```python
    # Create VPC
    vpc = ec2.Vpc(
        scope=self,
        id='CDKJobScrapingFrontend',
        vpc_name=f'{VPC_NAME}',

        # set the CIDR for the VPC
        cidr= '10.0.0.0/16',

        # enable DNS support
        enable_dns_support=True,

        # setup 2 subnet
        subnet_configuration=[

            # public subnet
            ec2.SubnetConfiguration(
                name="CDKJobScrapingFrontendPublic",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24,
            ),

            # private subnet with NAT
            ec2.SubnetConfiguration(
                name="CDKJobScrapingFrontendPrivate",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                cidr_mask=24,
            ),
        ],

    )

```

## Tạo Security Group cho EC2 Instance và Bastion Host
```python
        # +++ Create Ec2 +++

        # create a security group for the ec2 private instance
        private_ec2_security_group = ec2.SecurityGroup(
            scope=self,
            id="CDKJobScrapingFrontendSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security Group for the EC2 private instance",
            security_group_name="CDK-JobScraping-Frontend-Private-SG",
            
        )

        # add the ingress rule to the security group, open custom TPC port 8501
        private_ec2_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8501),
            description="Allow inbound traffic from anywhere for port 8501",
        )

        # add ssh port 22 for for SG for the EC2 private instance
        private_ec2_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow inbound traffic from anywhere for port 22",
        )


        # create security group for bastion host
        bastion_security_group = ec2.SecurityGroup(
            scope=self,
            id="CDKJobScrapingFrontendBastionSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security Group for the bastion host",
            security_group_name="CDK-JobScraping-Frontend-Bastion-SG",
            
        )

        # add the ingress rule to the security group, open SSH port 22
        bastion_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow inbound traffic from anywhere for port 22",
        )

```

## Tạo Bastion Host
Lưu ý: do mình không tìm được cách download key pem khi dùng CDK, nên bạn sẽ phải tạo sẵn 1 key pem và lưu tên vào biến môi trường nhé.
```python
    # create a bastion host

    # AMI for bastion host
    ami_bastion_host = ec2.MachineImage.generic_linux(
        {
            "us-east-1":"ami-053b0d53c279acc90"
        }
    )

    # DON'T FORGET THAT YOU WILL NEED TO CREATE A KEY PAIR IN THE AWS CONSOLE (BECAUSE YOU COULDN'T ACCESS IT LATTER IF CREATE HERE)
    bastion_host = ec2.Instance(
        scope=self,
        id="CDKJobScrapingFrontendBastionHost",
        instance_type=ec2.InstanceType("t2.micro"),
        machine_image=ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        ),
        vpc=vpc,
        vpc_subnets=ec2.SubnetSelection(
            subnet_type=ec2.SubnetType.PUBLIC
        ),
        security_group=bastion_security_group,
        key_name=f'{KEY_NAME}',
        instance_name='CDKJobScrapingFrontendBastionHost',
    )

```

## Tạo ASG và ALB

Trong đoạn code dưới, mình đã:
  
 - Tạo 1 role cho ASG
 - Tạo Launch Instance. Cần gán key pem nếu như muốn truy cập vào instance sau này. Launch Instance cũng cần SG. Đồng thời cần gán User Data cho Launch template
 - Tạo ASG
 - Tạo ALP
 - Tạo Target Group và gán ASG vào Target Group

```python

        # +++ Create Load Balancer and Auto Scaling Group +++

        # But first, we will need 2 things
        # 1. Create an AMI that have all the packages installed
        # 3. Create a Role for ASG

        # Since the first steps would be done in console, I'll do the 3rd step here
        
        # Create a role for ASG
        role = iam.Role(
            scope=self,
            id='CDKJobScrapingFrontendRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            role_name='CDKJobScrapingFrontendRole',
            managed_policies=[
                # Read access to Ec2
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ReadOnlyAccess'),

                # Full access to S3
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),

            ]
        )


        # Okay, now let move on to create the Load Balancer and Auto Scaling Group


        # Create Launch Template. Don't Forget a Key Pair
        launch_template = ec2.LaunchTemplate(
            scope=self,
            id='CDKJobScrapingFrontendLaunchTemplate',
            launch_template_name='CDKJobScrapingFrontendLaunchTemplate',        

            # set the machine image from the AMI that we created
            machine_image=ec2.MachineImage.generic_linux(
                {
                    "us-east-1":f'{AMI}'
                }
            ),

            # set the instance type
            instance_type=ec2.InstanceType("t2.micro"),

            # set the key pair
            key_name=f'{KEY_NAME}',

            # set the security group
            security_group=private_ec2_security_group,

            # set the role
            role=role,

            # set the block device mapping: use AMI block device mapping
            user_data=ec2.UserData.custom(         
'''Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash

# Run the app.py script
cd /home/ubuntu/

sudo streamlit run streamlit-app.py > output.txt 2>&1

--//--'''
            ),
        )


        # Create Auto Scaling Group
        auto_scaling_group = autoscaling.AutoScalingGroup(
            scope=self,
            vpc=vpc,
            id='CDKJobScrapingFrontendAutoScalingGroup',

                        

            # set the name for the Auto Scaling Group
            auto_scaling_group_name='CDKJobScrapingFrontendAutoScalingGroup',

            # set launch template
            launch_template = launch_template,
                
            # VPC private subnet
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT # current we since we only have 2 private sbunet, so can use this to select all
            ),

            # set the min, max, and desired capacity
            min_capacity=0,
            max_capacity=2,
            desired_capacity=1,

            

        )
        
        # create a load balancer
        load_balancer = elbv2.ApplicationLoadBalancer(
            scope=self,
            id='CDKJobScrapingFrontendLoadBalancer',
            vpc=vpc,
            internet_facing=True,
            load_balancer_name='CDKJobScrapingFrontendLB',
            security_group=private_ec2_security_group,
        )

        # create a target group that target to the Auto Scaling Group

        target_group = elbv2.ApplicationTargetGroup(
            scope=self,
            id='CDKJobScrapingFrontendTargetGroup',
            vpc=vpc,
            port=8501,
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[auto_scaling_group],
            target_group_name='CDKJobScrapingFrontendTG',
        )    

            
        # create a listener that listen to the target group
        listener = load_balancer.add_listener(
            id='CDKJobScrapingFrontendListener',
            port=8501,
            protocol=elbv2.ApplicationProtocol.HTTP,
            open=True,
            default_target_groups=[target_group],
        )

```