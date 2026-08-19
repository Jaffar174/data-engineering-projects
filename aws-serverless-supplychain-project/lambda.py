import boto3

glue_client = boto3.client('glue')

def lambda_handler(event, context):

    response = glue_client.start_job_run(
        JobName='supplychainetljob'
    )

    return {
        'statusCode': 200,
        'jobRunId': response['JobRunId']
    }
