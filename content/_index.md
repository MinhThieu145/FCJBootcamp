---
title : "Introduction and Preparation"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 1 </b> "
---

## General Introduction
Welcome to Workshop 1. In this workshop, I will design a simple crawler architecture so that you can crawl job postings on Indeed. This lab will be divided into three main parts:

### 1. CI/CD Pipeline Design
Part 1 of the lab will be about the CI/CD process of crawler. I will use **CodeBuild** to automatically get code from Githubm to build Docker image for crawler and automatically push the image into ECR. The architectural part will design as follows:

![](/images/third.png)

### 2. Architectural design for crawler
Part 2 of the lab, which is also the main part, will be about running the crawler as a Docker image using **Fargate. I will also provide code for crawlers. Crawler is written in Python and Selenium. You can also expand to create crawlers for other websites or modify existing crawlers as you like. The architecture includes AWS EventBridge** to be able to run a scheduled crawler, **AWS Lambda to send job definition to the job queue in the AWS Batch**. Once completed, the results will be stored in S3. The design architecture is as follows:

![](/images/second.png)

### 3. Design a front-end webapp to display the results
Part 3 of the lab will focus on designing a high-availability webapp to display crawler results. I will use Streamlit and write in Python. The webapp will be placed in EC2. The design architecture is as follows:
![](/images/forth.png)

