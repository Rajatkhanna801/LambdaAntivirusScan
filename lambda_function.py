import boto3
import requests
import update_result


def lambda_handler(event, context):
    """
        Lambda function used to run clamAV antivirus invoke when new s3 file is added.
    """
    # Get the bucket and object information from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3 = boto3.client('s3')
    # ClamAv virus scan API endpoint
    ec2_api_url = ""
    # Build the API request payload
    payload = {"s3_bucket": bucket,"s3_key": key}
    try:
        response = requests.post(ec2_api_url, json=payload)
        scan_result = response.json()
        virus_status = scan_result['virus_status']
        if virus_status == 'clean':
            destination_bucket = ""
            # Copy the file to the destination bucket
            s3.copy_object(
                Bucket=destination_bucket,
                Key=key,
                CopySource={'Bucket': bucket, 'Key': key}
            )
            # Delete the file from the initial bucket
            s3.delete_object(Bucket=bucket, Key=key)
        else:
            print('File is infected.')
        update_result(virus_status, key)
    except Exception as e:
        print("Exception = ", e)