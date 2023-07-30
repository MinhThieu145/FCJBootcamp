---
title : "Network Environment Design"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 3.1. </b> "
---

The first step is to design a network environment for the app. As mentioned earlier, here are the resources we will create:
- 2 public subnets, 2 private subnets
- 1 VPC
- 1 Internet Gateway
- 1 NAT Gateway (can create 2 NAT Gateways if you want to be more secure - each NAT in 1 subnet)
- S3 Endpoint to access S3 without going through NAT Gateway

## Setup VPC and Subnet

1. Select VPC, Create VPC. Select the option VPC and more**. Name the VPC. You can defaul CIDR: 10.0.0.0/16, you can also replace CIDR to increase and decrease the number of IPs in VPC. You can leave IPV6 as default (not using IPV6)
![](/images/2023-07-09-19-21-49.png)

1. **Number of Availability Zones: ** the number of AZ that the VPC will be generated. According to the diagram, I will leave 2 AZ. You can also choose Customize AZs to select other AZ (default is us-east-1a and us-east-1b if you use us-east-1)
![](/images/2023-07-09-19-30-53.png)

1. **Number of public subnets: ** How many public subnets in VPC? I need 2 public subnets (each AZ 1 public subnet) so I will leave 2. The graph on the right also shows each part of the public subnet: each AZ has a subnet, the subnet is passed through the Route table to connect to the Internet Gateway.
![](/images/2023-07-09-19-33-45.png)

1. **Number of private subnets: How many private subnets in VPC? I also need 2 private (1 AZ 1 private). If you choose 4, you can see the number of private subnets increase by 1 per AZ 
![](/images/2023-07-09-19-36-30.png)

1. **Customize subnets CIDR blocks: ** You can adjust this parameter to increase and decrease the number of IP addresses per subnet. Currently, each submet has 4096 IPs
![](/images/2023-07-09-19-39-17.png)

1. **NAT gateways ($) ** This is quite expensive part. If you want to be safe and according to the diagram, you can choose **1 per AZ** so that each AZ has 1 NAT. You can also select **In 1 AZ** to create only one NAT gateway for both private subnets.

2. **VPC endpoints** Should be selected to reduce S3 access costs. If you use boto3 without an Endpoint, you have to forcibly pass through NAT (due to data being transmitted to the internet). Having Endpoint will reduce the cost of NAT (if you don't really need the Internet) and data transfer fees.

3. DNS options** choose both options

4. Select Create VPC to complete.


