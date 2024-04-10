import boto3
from datetime import  datetime

def get_month_start(month: datetime) -> str:
    first_day =  month.replace(day=1)
    return first_day.strftime("%Y-%m-%d")

def list_s3_files(bucket_name, prefix, s3_client):
    # Use the paginator to handle large result sets
    paginator = s3_client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    # Iterate through the pages and list the files
    file_list = []

    for page in result:
        if 'Contents' in page:
            for obj in page['Contents']:
                file_list.append(obj['Key'])

    return file_list

def read_txt_from_s3(bucket_name, key, s3_client):
    try:
        # Read the JSON file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        return content

    except Exception as e:
        print(f"Error reading .txt from S3: {e}")
        return None
    
def put_object_to_s3(string, path, bucket, s3_client):
    s3_client.put_object(
        Body=string,
        Bucket=bucket,
        Key=path
    )

def reduce_month(
        month,
        output_bucket,
        clean_prefix,
        reduced_prefix
):
    s3_client = boto3.client('s3')

    month = get_month_start(month)
    month_parts = month.split('-')

    files = list_s3_files(output_bucket, f'{clean_prefix}{month_parts[0]}/{month_parts[1]}', s3_client=s3_client)

    for index,file in enumerate(files):
        print(f"Deciding to keep file {index+1} of {len(files)}")
        if file.endswith('.txt'):
            contents = read_txt_from_s3(output_bucket, file, s3_client)
            titles_part, body = contents.split('\n\n', 1)
            title = titles_part.split('\n', 1)[0]

            if len(title) > len(body):
                # this is a case of a short decision
                # typically meaning that it is just a holder for documents.
                # if we decide to store the documents then it may make more sense to keep those decisions
                print(f"dropping {file}")
                continue

            put_object_to_s3(
                contents,
                f'{reduced_prefix}{month_parts[0]}/{month_parts[1]}/{file.split("/")[-1]}',
                output_bucket,
                s3_client
            )