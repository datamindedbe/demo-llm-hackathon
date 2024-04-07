from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging
import json
import sys
import html2text
import re
import boto3

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

def read_json_from_s3(bucket_name, key, s3_client):
    try:
        # Read the JSON file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')

        # Parse the JSON content
        data = json.loads(content)

        return data

    except Exception as e:
        print(f"Error reading JSON from S3: {e}")
        return None
    
def get_attribute_string(contents, attribute_name):
    attribute = ''
    try:
        if attribute_name in contents['attributes'] and contents['attributes'][attribute_name] is not None:
            attribute_content = contents['attributes'][attribute_name]
            if isinstance(attribute_content, list):
                attribute_content = attribute_content[0]
            attribute_content = remove_markdown(remove_html_tags(attribute_content)).strip()
            return attribute_content
    except Exception as e:
        print(e)
        print(f"Error reading attribute {attribute_name}")
    return attribute

def remove_markdown(input_text):
    # Remove inline links
    text_without_links = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', input_text)
    
    # Remove images
    text_without_images = re.sub(r'\!\[([^\]]*)\]\([^\)]*\)', '', text_without_links)
    
    # Remove headings
    text_without_headings = re.sub(r'#{1,6}\s', '', text_without_images)
    
    # Remove bold and italic formatting
    text_without_formatting = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text_without_headings)
    text_without_formatting = re.sub(r'(\*|_)(.*?)\1', r'\2', text_without_formatting)

    return text_without_formatting

def remove_html_tags(input_html):
    # Convert HTML to plain text
    text = html2text.html2text(input_html)
    
    return text

def extract_date_from_datetime(datetime_string):
    # Convert the string to a datetime object
    dt_object = None
    try:
        dt_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    except:
        try:
            dt_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            pass

    if dt_object is None:
        return None
    
    # Extract the date-only part
    date_only = dt_object.date()

    return date_only

def put_object_to_s3(jsonstring, path, s3_client, bucket_name):
    s3_client.put_object(
        Body=jsonstring,
        Bucket=bucket_name,
        Key=path
    )



def clean_month(
    month: datetime,
    output_bucket: str,
    raw_prefix: str,
    clean_prefix: str,
    aws_profile_name: str
):
    # set up the boto3 session
    boto3.setup_default_session(profile_name=aws_profile_name)
    s3_client = boto3.client('s3')

    month_start = get_month_start(month)
    month_parts = month_start.split('-')
    files = list_s3_files(output_bucket, f'{raw_prefix}{month_parts[0]}/{month_parts[1]}', s3_client=s3_client)
    for index, file in enumerate(files):
         print(f"Processing file {index + 1} of {len(files)}")
         if file.endswith('document.json'):
            contents = read_json_from_s3(output_bucket, file, s3_client=s3_client)
            if contents:
                title = get_attribute_string(contents, 'title')
                alternative_title = get_attribute_string(contents, 'alternativeTitle')
                body = get_attribute_string(contents, 'htmlContent')
                agenda_type = get_attribute_string(contents, 'agendaitemType').lower()
                uuid = get_attribute_string(contents, 'uuid')
                date = extract_date_from_datetime(contents['attributes']['meetingDate'])
                if date:
                    date = str(date)
                else:
                    date = month_start

                export_string = f'{title}\n{alternative_title}\n\n{body}'
                put_object_to_s3(
                    export_string,
                    f'{clean_prefix}{month_parts[0]}/{month_parts[1]}/{date}-{agenda_type}-{uuid}.txt',
                    s3_client=s3_client,
                    bucket_name=output_bucket
                )