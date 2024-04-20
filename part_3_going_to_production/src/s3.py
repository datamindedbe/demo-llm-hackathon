import boto3

s3_client= boto3.client('s3')

def read_txt_from_s3(bucket_name, key):
    try:
        # Read the JSON file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')

        return content

    except Exception as e:
        print(key)
        print(f"Error reading text file from S3: {e}")
        return None