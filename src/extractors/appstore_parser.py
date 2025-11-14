import json
import logging
import re
import requests
from .utils_date import parse_date

class AppStoreParser:
    BASE_URL = "https://itunes.apple.com/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"

    def extract_app_id(self, url: str) -> str:
        match = re.search(r"id(\d+)", url)
        if not match:
            raise ValueError("Invalid App Store URL — app ID not found.")
        return match.group(1)

    def fetch_reviews(self, app_url: str, limit: int = 200):
        app_id = self.extract_app_id(app_url)
        reviews = []
        page = 1

        while len(reviews) < limit:
            api_url = self.BASE_URL.format(page=page, app_id=app_id)
            logging.debug(f"Requesting {api_url}")
            response = requests.get(api_url, timeout=10)

            if response.status_code != 200:
                logging.warning(f"Bad response ({response.status_code}) from Apple API.")
                break

            data = response.json()
            entries = data.get("feed", {}).get("entry", [])

            # First entry is app metadata; skip it
            if entries and isinstance(entries, list):
                entries = entries[1:]

            if not entries:
                break

            for entry in entries:
                if len(reviews) >= limit:
                    break

                reviews.append({
                    "review_id": entry.get("id", {}).get("label"),
                    "username": entry.get("author", {}).get("name", {}).get("label"),
                    "rating": int(entry.get("im:rating", {}).get("label", 0)),
                    "title": entry.get("title", {}).get("label"),
                    "review_text": entry.get("content", {}).get("label"),
                    "date": parse_date(entry.get("updated", {}).get("label")),
                    "country": "US",
                    "app_url": app_url
                })

            page += 1

        return reviews