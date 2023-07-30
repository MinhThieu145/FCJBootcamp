---
title : "Clean up resources"
date :  "`r Sys.Date()`" 
weight : 5 
chapter : false
pre : " <b> 5. </b> "
---

## General Introduction
After completing the workshop. You need to delete resources to avoid additional costs. 

## Remove ASG
1. Go back to EC2 and select Auto Scaling Groups
2. Select the ASG you created and select Action -> Delete. Enter the word delete to confirm

## Delete Load Balancer
1. Go back to EC2, select Load Balancers (on Auto Scaling Groups 1 minute, right on target groups) 
2. Select the Load Balancer you created and select Action -> Delete Load Balancer. Type Confirm -> Delete
 
## Delete Target Group
1. Go back to EC2 and select Target Groups (on Auto Scaling Groups)
2. Select the Target Group you created and select Action -> Delete. Select Yes, Delete

## Delete the Instane 
1. Go to EC2 and select Instances
2. Select the running instances and select Instance state -> Terminate. 

## Delete AWS Batch Job Definition
1. Go to AWS Batch and select the Job definitions tab.
2. Select the Job Definition you created and select Deregister
   
## Delete AWS Batch Job Queue
1. Go to AWS Batch and select the Job Queues tab
2. Select the job queue you created and select Disable
3. After disabling, select the queue again and select Delete

## Removing the AWS Batch Compute Environment
1. In AWS Batch, select the Compute environments tab
2. Select the Compute Environment you created and select Disable
3. Select Compute Environment again and select Delete (wait a while until the job queue is deleted to delete the compute environment)

## Delete Codebuild Project
1. Go to AWS Codebuild
2. Select the project you created and select Delete build project
3. Enter delete to confirm, select Delete

## Delete the AWS ECR Repository
1. Enter AWS ECR
2. Select the repository you created and select Delete.
3. Enter delete to confirm, select Delete

## Delete VPC
1. Enter VPC
2. Select the VPC you created, Select Action -> Delete VPC
3. Enter delete to confirm, select Delete
