# this needs to be converted into an airflow dag and run on conveyor
from datetime import date
import os
from scrape import scrape_month
from clean import clean_month


def run_remove_short_decisions():
    # run the remove short decisions script
    pass


if __name__ == "__main__":

    SCRAPER_DECISIONS_START_DATE = date(2024, 1, 1)

    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX = 'test_hackathon/data/raw/'
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN = 'test_hackathon/data/clean/'
    SCRAPER_DECISIONS_OUTPUT_S3_BUCKET = 'electionsai'
    SCRAPER_DECISIONS_BASE_URL = "https://beslissingenvlaamseregering.vlaanderen.be"
    SCRAPER_DECISIONS_INFO_TEMPLATE = SCRAPER_DECISIONS_BASE_URL + "/news-items/search?page%5Bsize%5D=100&page%5Bnumber%5D={page}&collapse_uuids=f&filter%5B%3Agte%2Clte%3AmeetingDate%5D={start}T22%3A00%3A00.000Z%2C{end}T22%3A59%3A59.000Z&sort%5BmeetingDate%5D=desc&sort%5BmeetingTypePosition%5D=asc&sort%5BagendaitemType%5D=desc&sort%5Bposition%5D=asc"
    SCRAPER_DECISIONS_ATTACHMENT_TEMPLATE = SCRAPER_DECISIONS_BASE_URL + "/news-item-infos?filter%5B%3Aid%3A%5D={id}&include=attachments.file&page%5Bsize%5D=1"
    SCRAPER_DECISIONS_AWS_PROFILE_NAME= os.environ.get('AWS_PROFILE_NAME')

    scrape_month(
       month=SCRAPER_DECISIONS_START_DATE,
       output_bucket=SCRAPER_DECISIONS_OUTPUT_S3_BUCKET,
       output_prefix=SCRAPER_DECISIONS_OUTPUT_S3_PREFIX,
       info_template=SCRAPER_DECISIONS_INFO_TEMPLATE,
       aws_profile_name=SCRAPER_DECISIONS_AWS_PROFILE_NAME
    )

    clean_month(
        month=SCRAPER_DECISIONS_START_DATE,
        output_bucket=SCRAPER_DECISIONS_OUTPUT_S3_BUCKET,
        raw_prefix=SCRAPER_DECISIONS_OUTPUT_S3_PREFIX,
        clean_prefix=SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN,
        aws_profile_name=SCRAPER_DECISIONS_AWS_PROFILE_NAME
    )
    
    run_remove_short_decisions()