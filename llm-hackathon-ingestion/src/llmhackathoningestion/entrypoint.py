import argparse
import logging
import sys
from datetime import datetime

from llmhackathoningestion.task_logic.scrape  import scrape_month
from llmhackathoningestion.task_logic.clean  import clean_month
from llmhackathoningestion.task_logic.reduce  import reduce_month


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
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX = 'data/raw/'
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN = 'data/clean/'
    SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN_REDUCED = 'data/reduced/'

    day_in_month = datetime.strptime(args.date, "%Y-%m-%d") # the pipeline runs for the full month (day part is not important)

    if args.task == "scrape":
        scrape_month(day_in_month, args.bucket, SCRAPER_DECISIONS_OUTPUT_S3_PREFIX, SCRAPER_DECISIONS_INFO_TEMPLATE)
    elif args.task == "clean":
         clean_month(day_in_month, args.bucket, SCRAPER_DECISIONS_OUTPUT_S3_PREFIX, SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN)
    elif args.task == "reduce":
         reduce_month(day_in_month, args.bucket, SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN, SCRAPER_DECISIONS_OUTPUT_S3_PREFIX_CLEAN_REDUCED)


if __name__ == "__main__":
    main()
