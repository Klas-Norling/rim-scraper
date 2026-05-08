# Rim Scraper

A Python-based web scraper that extracts chapters from the online novel 'Regression Instruction Manual' and counts occurrences of a specific keyword across a range of chapters.


---

## Features

- Scrapes chapter-based web pages automatically
- Extracts main text content from HTML
- Counts occurrences of a target keyword
- Handles rate limiting (HTTP 429 responses)
- Uses persistent HTTP sessions for efficiency
- Configurable start/end chapter via command line
- Logging-based output

---

## How It Works

1. Builds chapter URLs dynamically  
2. Fetches HTML using `requests`
3. Parses content using `BeautifulSoup`
4. Extracts text from the page’s main content section
5. Tokenizes and cleans words
6. Counts keyword occurrences per chapter
7. Prints results per chapter and final summary

---

## Install dependencies
```bash
pip install requests beautifulsoup4
```

---

## Usage
### Default run:

```bash
python rim_scraper.py
```

### Start from a specific chapter:

```bash
python rim_scraper.py --start 600
```

### Define a chapter range:

```bash
python rim_scraper.py --start 600 --end 800
```
### Change the keyword being searched:
```bash
python rim_scraper.py --keyword "example"
```

### Adjust request delay:
```bash
python rim_scraper.py --delay 2
```

### Combine all options:
```bash
python rim_scraper.py --start 600 --end 800 --keyword "example" --delay 2
```

