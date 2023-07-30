---
title : "Designing AWS Batch and S3 to run crawlers and save results"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 2 </b> "
---

## Overview Introduction

Congratulations on completing the first part of the workshop. In this section, I will design AWS Batch to be able to automatically retrieve the images from the ECR repo that I made in the previous section and run according to the existing schedule. I will also create an S3 bucket to save the results. The services that I will use in this post:

- **AWS Batch: ** To run your task crawler
- **AWS S3: ** To store results
- **AWS EventBridge: ** To run scheduled tasks. If you only use AWS Batch, you will have to submit the job manually. So I will use EventBridge to automatically submit jobs to Batch according to the available schedule
- **AWS Lambda: ** However EventBridge can set schedules. However, for more features, I will use Lambda to submit jobs to Batch. Lambda will be triggered by EventBridge very easily. And Lambda itself, I'll use boto3 to connect to the batch and submit the job.

## Introduction to AWS Batch
AWS Batch is a serverless service that allows you to run batch jobs. AWS Batch will automatically scale smaller nodes. Helps you save money and run jobs faster. We'll go through each section of AWS Batch:

- **Compute Environment: ** This is the place for you to choose the compute resource that suits your needs. Since Batch is a serverless service, you won't have to setup too much
- **Job queue: ** 1 queue to contain jobs. When you submit jobs to the batch, the jobs will be in the queue
- **Job definition: ** is the *definition* of the job. You can imagine this is the drawing of the job you want to make. When you want to do this job definition**, you submit it to the queue.

## About S3
This is a well-known service of AWS. S3 is Object Storage Service S3 can save different file formats, code, video or images, etc.
