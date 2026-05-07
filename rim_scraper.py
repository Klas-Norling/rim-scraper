import argparse
import time
import string
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup


# ----------------------------
# Configuration
# ----------------------------

@dataclass
class ScraperConfig:
    base_url: str = "https://novelfire.net/book/regressor-instruction-manual/chapter-"
    start_chapter: int = 467
    end_chapter: int = 1531
    keyword: str = "Hee-ra"
    delay_seconds: float = 1.0
    timeout: int = 10


# ----------------------------
# Scraper
# ----------------------------

class NovelScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.session = self._create_session()
        self.results: Dict[int, int] = {}

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml",
        })
        return session

    # ----------------------------
    # Fetch HTML safely
    # ----------------------------

    def fetch_html(self, url: str, retries: int = 3) -> Optional[str]:
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=self.config.timeout)

                if response.status_code == 429:
                    wait = int(response.headers.get("Retry-After", 5))
                    logging.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue

                response.raise_for_status()
                return response.text

            except requests.RequestException as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        logging.error(f"Failed to fetch after {retries} attempts: {url}")
        return None

    # ----------------------------
    # Parse and analyze HTML
    # ----------------------------

    def count_keyword(self, html: str) -> int:
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", id="content")

        if not content:
            logging.warning("Content div not found.")
            return 0

        text = content.get_text(separator=" ", strip=True)
        words = text.split()

        count = 0
        for word in words:
            cleaned = word.strip(string.punctuation)
            if cleaned == self.config.keyword:
                count += 1

        return count

    # ----------------------------
    # Process one chapter
    # ----------------------------

    def process_chapter(self, chapter: int) -> None:
        url = f"{self.config.base_url}{chapter}"
        html = self.fetch_html(url)

        if not html:
            return

        count = self.count_keyword(html)
        self.results[chapter] = count

        logging.info(f"Chapter {chapter}: {count} occurrences")

    # ----------------------------
    # Main loop
    # ----------------------------

    def run(self) -> Dict[int, int]:
        for chapter in range(self.config.start_chapter, self.config.end_chapter + 1):
            self.process_chapter(chapter)
            time.sleep(self.config.delay_seconds)

        return self.results



# ----------------------------
#             CLI
# ---------------------------
# Examples:

# Default run:
#   python rim_scraper.py

# Custom start chapter:
#   python rim_scraper.py --start 600

# Custom range + keyword:
#   python rim_scraper.py --start 600 --end 800 --keyword "Hee-ra"
#------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Novel chapter scraper")

    parser.add_argument(
        "--start",
        type=int,
        default=467,
        help="Starting chapter number"
    )

    parser.add_argument(
        "--end",
        type=int,
        default=1531,
        help="Ending chapter number"
    )

    parser.add_argument(
        "--keyword",
        type=str,
        default="Hee-ra",
        help="Keyword to search for"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests (seconds)"
    )

    return parser.parse_args()


# ----------------------------
# Entry point
# ----------------------------

if __name__ == "__main__":
    args = parse_args()

    config = ScraperConfig(
        start_chapter=args.start,
        end_chapter=args.end,
        keyword=args.keyword,
        delay_seconds=args.delay
    )

    scraper = NovelScraper(config)
    results = scraper.run()

    print("\nFinal summary:")
    for chapter, count in results.items():
        print(f"Chapter {chapter}: {count}")