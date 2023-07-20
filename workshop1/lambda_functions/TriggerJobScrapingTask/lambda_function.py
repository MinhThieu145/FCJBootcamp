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