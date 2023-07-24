---
title : "Tạo lịch trình để submit job bằng EventBridge và lưu kết quả vào S3"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 2.2 </b> "
---

Sau khi hoàn thành bước trước, bạn đã có 1 job setup hoàn chỉnh trên Batch. Nhưng để chạy job, bạn cần submit job. Bạn có thể submit job thủ công bằng cách vào Batch, chọn job và Submit new Job
![](/images/2023-07-09-17-48-10.png) 

Tuy nhiên, nếu bạn cần submit job mỗi ngày, hay theo một lịch trình cố định hay theo một trigger nào đó thì việc submit job thủ công là không khả thi. Vì vậy, chúng ta sẽ tạo 1 schedule để tự động submit job. Để làm được điều này, chúng ta sẽ sử dụng Cloudwatch Event và Lambda để tạo 1 schedule và submit job.

## Tạo Lambda
Vào Lambda, chọn **Create function**
![](/images/2023-07-09-17-50-43.png)

1. Có thể để là **Default from Scrach** do function khá đơn giản, chọn tên, **Runtime** và **Architecture** để là **x86_64**
![](/images/2023-07-09-17-56-23.png)

2. Chọn **Change default execution role** do bạn cần thêm role cho function để có thể submit job. 
![](/images/2023-07-09-17-59-30.png)
Vào IAM vào thêm policy **AWSBatchServiceEventTargetRole** cho role
![](/images/2023-07-09-18-00-44.png)

3. Sau khi tạo xong role, có thể chọn Create function

4. Sau khi tạo xong function, paste đoạn code sau vào function

```python

import boto3
import os

def lambda_handler(event, context):
    # client
    batch_client = boto3.client('batch')
    
    # load from the environment variables of lambda
    job_name = os.getenv("JOB_NAME")
    job_queue = os.getenv("JOB_QUEUE")
    job_definition = os.getenv("JOB_DEFINITION")
        
    response = batch_client.submit_job(
        jobName=job_name,
        jobQueue=job_queue,
        jobDefinition=job_definition,
        
    )
    
    if 'jobId' in response:
        return {
            'statusCode': 200,
            'body': f"Job submitted successfully. Job ID: {response['jobId']}"
        }
    else:
        return {
            'statusCode': 500,
            'body': 'Failed to submit job to AWS Batch'
        }

```
Đồng thời, bạn cần thay các giá trị của **job_name**, **job_queue** và **job_definition** bằng giá trị tương ứng ban nãy trong AWS Batch

## Tạo S3 bucket để lưu kết quả
Trong workshop này, mình lưu kết quả bằng boto3 vào 1 bucket tên là **job-description-process**, bên trong bucket đó, mình sẽ tạo 1 folder tên là **indeed-scraper** và lưu kết quả. Bạn cần vào file `job_description_analyzer.py` ở github clone ban nãy và sửa giá trị của *BUCKET_NAME_RESULT* thành tên của riêng bạn. Lý do là vì S3 là dịch vụ global, và tên bucket phải là duy nhất, không thể trùng. 

1. Vào S3, Create bucket
![](/images/2023-07-09-18-24-49.png)

1. Chọn tên tuỳ ý và để phàn còn lại là default
![](/images/2023-07-09-18-26-08.png)

1. Chọn Create bucket

## Tạo Event Bridge
1. Vào Event Bridge, chọn **Schedules**
![](/images/2023-07-09-18-31-08.png)

2. Chọn Create Schedule
![](/images/2023-07-09-18-31-44.png)

3. Sau khi đặt tên cho schedule, ở phần **Occurence** chọn Recurring Schedule, **Schedule Type** là Cron-based và điền Cron như sau
```cron
0 6 ? * * *
```

4. Chọn Flexible time window là Off và chọn Next
![](/images/2023-07-09-18-34-39.png)
 

5. Chọn target là AWS Lambda và chọn Lambda Function vừa tạo và Next
![](/images/2023-07-09-18-53-19.png)

1. Để default options ở trang tiếp theo, chọn next và cuối cùng là Create sau khi review

