import argparse
import logging
import sys

import requests
from typing import Optional

from datetime import date
import os
from llmhackathoningestion.scrape  import scrape_month
from llmhackathoningestion.clean  import clean_month
from llmhackathoningestion.reduce  import reduce_month


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description="llm-hackathon-ingestion")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )
    parser.add_argument(
        "-t", "--task", dest="task", help="which task to run", required=True
    )
    parser.add_argument(
        "-b", "--bucket", dest="bucket", help="bucket to use", required=True
    )
    args = parser.parse_args()
    logging.info(f"Using args: {args}")

    SCRAPER_DECISIONS_BASE_URL = "https://beslissingenvlaamseregering.vlaanderen.be"
    SCRAPER_DECISIONS_INFO_TEMPLATE = SCRAPER_DECISIONS_BASE_URL + "/news-items/search?page%5Bsize%5D=100&page%5Bnumber%5D={page}&collapse_uuids=f&filter%5B%3Agte%2Clte%3AmeetingDate%5D={start}T22%3A00%3A00.000Z%2C{end}T22%3A59%3A59.000Z&sort%5BmeetingDate%5D=desc&sort%5BmeetingTypePosition%5D=asc&sort%5BagendaitemType%5D=desc&sort%5Bposition%5D=asc"
    SCRAPER_DECISIONS_ATTACHMENT_TEMPLATE = SCRAPER_DECISIONS_BASE_URL + "/news-item-infos?filter%5B%3Aid%3A%5D={id}&include=attachments.file&page%5Bsize%5D=1"
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX = 'test_hackathon/data/raw/'
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN = 'test_hackathon/data/clean/'
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN_REDUCED = 'test_hackathon/data/reduced/'

    if args.task == "scrape":
        scrape_month(args.date, args.bucket, SCRAPER_DECISIONS_OUTPUT_S3_PREFIX, SCRAPER_DECISIONS_INFO_TEMPLATE)
    # elif args.task == "clean":
    #     clean_month(args.env, args.date, args.bucket)
    # elif args.task == "reduce":
    #     reduce_month(args.env, args.date, args.bucket)


if __name__ == "__main__":
    main()
