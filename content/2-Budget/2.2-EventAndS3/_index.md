---
title : "Create a schedule to submit jobs using EventBridge and save the results to S3"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 2.2 </b> "
---

After completing the previous step, you already have a complete job setup on the batch. But in order to run a job, you need to submit the job. You can submit a job manually by going to Batch, selecting a job, and Submit a new job.
![](/images/2023-07-09-17-48-10.png) 

However, if you need to submit jobs every day, on a fixed schedule or follow a certain trigger, manual job submission is not feasible. So we're going to create a schedule to automatically submit jobs. To do this, we'll use Cloudwatch Event and Lambda to create a schedule and submit the job.

## Create Lambda
Go to Lambda and select Create function**
![](/images/2023-07-09-17-50-43.png)

1. It can be left as **Default from Scrach** because the function is quite simple, select the name, **Runtime** and **Architecture** to be **x86_64**
![](/images/2023-07-09-17-56-23.png)

2. Select Change default execution role because you need to add roles to the function in order to submit the job. 
![](/images/2023-07-09-17-59-30.png)
Go to IAM and add the policy **awsBatchServiceEventTArgetTrole** for the role
![](/images/2023-07-09-18-00-44.png)

3. Once you've created your role, you can choose Create function.

4. After creating the function, paste the following code into the function

```python

import boto3
import os

def lambda_handler (event, context):
# client
batch_client = boto3.client ('batch')
    
# load from the environment variables of lambda
job_name = os.getenv (“JOB_NAME”)
job_queue = os.getenv (“JOB_QUEUE”)
job_definition = os.getenv (“JOB_DEFINITION”)
        
response = batch_client.submit_job (
jobname=Job_name,
JobQueue=Job_Queue,
Jobdefinition=Job_definition,
        
)
    
if 'Jobid' in response:
return {
'StatusCode': 200,
'body': F"Job submitted successfully. Job ID: {response ['JoBid']}”
}
else:
return {
'statusCode': 500,
'body': 'Failed to submit job to AWS Batch'
}

```
At the same time, you need to replace the values of **job_name, **job_queue, and **job_definition** with the corresponding values earlier in AWS Batch

## Create S3 bucket to save results
In this workshop, I save the results with boto3 in a bucket named **job-description-process**, inside that bucket, I will create a folder named **indeed-scraper** and save the result. You need to go to the `job_description_analyzer.py` file in the github clone earlier and edit the value of *BUCKET_NAME_RESULT* to your own name. The reason is that S3 is a global service, and the bucket name must be unique and cannot be the case. 

1. Go to S3, Create Bucket
![](/images/2023-07-09-18-24-49.png)

1. Select the name of your choice and leave the rest as default
![](/images/2023-07-09-18-26-08.png)

1. Select Create Bucket

## Create Event Bridge
1. Go to Event Bridge and select Schedules
![](/images/2023-07-09-18-31-08.png)

2. Select Create Schedule
![](/images/2023-07-09-18-31-44.png)

3. After naming the schedule, in the Occupancy section select Recurring Schedule, the Schedule Type is Cron-based and fill in the Cron as follows.
```cron
0 6? ***
```

4. Select the Flexible Time Window to Off and select Next
![](/images/2023-07-09-18-34-39.png)
 

5. Select AWS Lambda target and select Lambda Function just created and Next
![](/images/2023-07-09-18-53-19.png)

1. For default options on the next page, select Next and finally Create after review

