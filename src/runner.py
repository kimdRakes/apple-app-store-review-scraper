import argparse
import json
import logging
import os
from pathlib import Path

from extractors.appstore_parser import AppStoreParser
from outputs.exporters import JSONExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_urls(input_path: str):
    with open(input_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Apple App Store Review Scraper")
    parser.add_argument("--input", "-i", required=True, help="Path to input file containing app URLs")
    parser.add_argument("--output", "-o", default="data/output.json", help="Output JSON file")
    parser.add_argument("--limit", "-l", type=int, default=200, help="Max reviews per app")

    args = parser.parse_args()

    urls = load_urls(args.input)
    scraper = AppStoreParser()
    exporter = JSONExporter()

    all_reviews = []
    for url in urls:
        logging.info(f"Scraping: {url}")
        try:
            reviews = scraper.fetch_reviews(url, limit=args.limit)
            all_reviews.extend(reviews)
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {e}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    exporter.export(args.output, all_reviews)
    logging.info(f"Saved {len(all_reviews)} reviews to {args.output}")

if __name__ == "__main__":
    main()