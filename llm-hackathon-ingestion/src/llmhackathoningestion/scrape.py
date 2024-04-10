import requests
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from requests.adapters import HTTPAdapter, Retry
import logging
import boto3


def get_month_start(month: datetime) -> str:
    first_day =  month.replace(day=1)
    return first_day.strftime("%Y-%m-%d")

def get_month_end(month: datetime) -> str:
    last_day =  month.replace(day=1) + relativedelta(months=1, days=-1)
    return last_day.strftime("%Y-%m-%d")

def try_get_url(url):
    downloaded = False
    while not downloaded:
        try: 
            retries = Retry(total=10,
                            backoff_factor=1,
                            status_forcelist=[ 500, 502, 503, 504 ])
            s = requests.Session()
            s.mount('https://', HTTPAdapter(max_retries=retries))
            response = s.request("GET", url, timeout=10)
            downloaded = True
            return response
        except Exception as ex:
            logging.info(f"\tDownload failed: {ex}")
            logging.info(f"\tRetrying...")

def store_news_contents(month, contents, s3_prefix, s3_bucket, s3_client):
    month = month.replace("-", "/")
    for item in contents['data']:
        base_path = s3_prefix + month + item["id"] + "/" 
        json_path = base_path + "document.json"
        store_json(item, json_path, s3_bucket, s3_client)

def store_json(item, path, output_bucket, s3_client):
    jsonstring = json.dumps(item, indent=4)
    put_object_to_s3(jsonstring, path, output_bucket, s3_client)
    logging.info(path)

def put_object_to_s3(jsonstring, path, output_bucket, s3_client):
    s3_client.put_object(
        Body=jsonstring,
        Bucket=output_bucket,
        Key=path
    )

def scrape_month(
       month_str :str,
       output_bucket :str,
       output_prefix : str,
       info_template :str,
    ):


    month = datetime.strptime(month_str, "%Y-%m-%d")
    # set up the boto3 session
    s3_client = boto3.client('s3')


    # do a full scrape for the month indicated in the date
    start_date = get_month_start(month)
    end_date = get_month_end(month)
    
    page_count = 0    
    page_size = 100
    processed = 0
    total = 0
    start = True
    while processed < total or start:
        start = False
        url = info_template.format(start=start_date,end=end_date, page = page_count)
        page = try_get_url(url)
        contents = json.loads(page.text)        
        store_news_contents(start_date[:8], contents, s3_prefix=output_prefix, s3_bucket=output_bucket, s3_client=s3_client)
        total = contents['count']
        processed += len(contents['data'])
        page_count += 1
    logging.info(f"Stored {processed} items from {start_date} to {end_date}")