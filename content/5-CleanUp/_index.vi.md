---
title : "Dọn dẹp tài nguyên"
date :  "`r Sys.Date()`" 
weight : 5 
chapter : false
pre : " <b> 5. </b> "
---

## Giới thiệu tổng quát
Sau khi hoàn thành workshop. Bạn cần xoá đi tài nguyên để tránh phát sinh thêm chi phí. 

## Xoá ASG
1. Vào lại Ec2, chọn Auto Scaling Groups
2. Chọn ASG bạn đã tạo và chọn Action -> Delete. Nhập chữ delete để xác nhận

## Xoá Load Balancer
1. Vào lại EC2, chọn Load Balancers (trên Auto Scaling Groups 1 xíu, ngay trên target groups) 
2. Chọn Load Balancer bạn đã tạo và chọn Action -> Delete Load Balancer. Gõ confirm -> Delete
 
## Xoá Target Group
1. Vào lại EC2, chọn Target Groups (trên Auto Scaling Groups)
2. Chọn Target Group bạn đã tạo và chọn Action -> Delete. Chọn Yes, delete

## Xoá những Instane 
1. Vào Ec2, chọn Instances
2. Chọn những instance đang chạy và chọn Instance state -> Terminate. 

## Xoá AWS Batch Job Definition
1. Vào AWS Batch, chọn tab Job definitions
2. Chọn Job Definition bạn đã tạo và chọn Deregister
   
## Xoá AWS Batch Job Queue
1. Vào AWS Batch, chọn tab Job queues
2. Chọn Job Queue bạn đã tạo và chọn Disable
3. Sau khi disable, chọn lại queue và chọn Delete

## Xoá AWS Batch Compute Environment
1. Vào AWS Batch, chọn tab Compute environments
2. Chọn Compute Environment bạn đã tạo và chọn Disable
3. Chọn lại Compute Environment và chọn Delete (phải đợi 1 lúc cho đến khi job queue xoá xong thì mới xoá được compute environment)

## Xoá Codebuild Project
1. Vào AWS Codebuild
2. Chọn Project bạn đã tạo và chọn Delete build project
3. Nhập delete để confirm, chọn Delete

## Xoá AWS ECR Repository
1. Vào AWS ECR
2. Chọn Repository bạn đã tạo và chọn Delete
3. Nhập delete để confirm, chọn Delete

## Xoá VPC
1. Vào VPC
2. Chọn những VPC bạn đã tạo, Chọn Action -> Delete VPC
3. Nhập delete để confirm, chọn Delete
