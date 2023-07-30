---
title : "Create a Frontend Webapp to see the results"
date :  "`r Sys.Date()`" 
weight : 3 
chapter : false
pre : " <b> 3. </b> "
---

## Overview Introduction
If you have made it here, congratulations on almost completing the workshop. In previous sections, Crawler was able to run on a schedule and save the results to S3. However, there is still no way you can view those results conveniently, or share them with others. In this article, I will continue to design a streamlit webapp to display results from S3.

## Introduction to Streamlit
Streamlit is an open-source library that uses python to build webapps. Streamlit is primarily used to share data science results. However, you can use it to build webapps for other purposes. Streamlit can run locally or in the cloud. In this post, I will run on EC2.

## Architectural Design
Because this part of the structure is a bit long, I will go very carefully. First of all, read the diagram architecture of this section. I will go in the order in which the client will go (i.e. go from the client side to the server side).
![](/images/forth.png)

### 1. Application Load Balancer
First, the user will access the DNS of the Application Load Balancer (ALB) through the browser. ALB will redirect the request to the Auto Scaling Group, from which access the app is placed in the private subnet. The ALB itself must be placed in the public subnet, as it will receive requests from the internet. The app will be placed in the private subnet because it will receive requests from ALB.

{{% notice note%}}
*AWS Elastic Load Balancer (ELB) service at a glance: * ELB is an AWS load balancing service. It allows distributing requests to instances to ensure performance and reliability. ELBs can help prevent instances from being overloaded by dividing requests evenly, or using health checks to avoid requests to defective instances. In this article, I will use the load balancing type which is **Application Load Balancer**. This is a load balancing in layer 7, which supports distribution based on the header, protocol of the request.
{{% /notice%}}

### 2. Auto Scaling Group
After the user accesses the ALB's DNS, the ALB will redirect the request to the Auto Scaling Group. The Auto Scaling Group (ASG) is responsible for creating instances to run the app. The created instances will be placed in the private subnet.

{{% notice note%}}
*AWS Auto Scaling Group (ASG) Service Outline: * AWS ASG is a service that allows automatic expansion or narrowing of instances based on presets and instance status. Auto Scaling Group helps keep the system from overloading, cutting costs and increasing availability. Auto Scaling Group will automatically generate additional EC2 istances, increase the number of EC2 instances as traffic increases and reduces the number of EC2 instances as traffic decreases, while replacing health check failed instances. These instances are created and deleted automatically, so an ELB is required to direct traffic to them.
{{% /notice%}}

### 3. Design network system for app.
For safety, the architecture is placed in the VPC, separated into 2 AZ. You can see 2 AZ (us-east-1c and us-east-1d) identical. This is to keep the system running even though the AZ is down. There are 4 subnets in the VPC, 2 public and 2 private. In one of the two public subnets, I have 1 EC2 for the purpose of being a Bastion Host. 

{{% notice note%}}
*Bastion Host* is a better way to protect the system by placing resources in the private subnet, and access from outside will have to go through the Bastion Host to get inside (SSH access, the rest if using ALB's DNS, go through ALB).  
{{% /notice%}}
The remaining 2 private subnets, I set ASG. ASG automatically creates ec2 instances in these two private subnets and directs its request from the outside.
