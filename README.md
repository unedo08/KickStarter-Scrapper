# Kickstarter Scrapper
Kickstarter Scraper is a tool for scraping the [Kickstarter](https://www.kickstarter.com/) web. This tool uses project datasets on Kickstarter by Web Robots namely [Kickstarter Datasets](https://webrobots.io/kickstarter-datasets/) as inputs to scrape text data on the _Campaign_, _FAQ_, _Updates_, _Comments_, and _Community_.

## Libraries
The following is a list of the Python libraries required to run this tool.
* json
* re
* time
* os
* pandas - versi 1.3.4
* selenium - versi 4.1.2
* webdriver_manager - versi 3.5.2
* beautifulsoup4 - versi 4.10.0

## Usage
1. Make a directory namely `chromedriver`.
2. Download ChromeDriver from https://chromedriver.chromium.org/downloads, unzip it, and store `chromedriver.exe` inside `chromedriver` directory.
3. Run this command `python src\main.py kickstarter-corpus.json`