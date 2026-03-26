# DIAGNOSTIC 2 - inspect a single year page
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def diagnose_year_page():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)

    url = "https://www.exchange-rates.org/exchange-rate-history/idr-gbp/2024"
    print(f"Loading: {url}")
    driver.get(url)
    time.sleep(8)  # Give it lots of time

    print(f"Title: {driver.title}")
    print(f"Current URL: {driver.current_url}")

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Check for tables
    tables = soup.find_all("table")
    print(f"\nTables found: {len(tables)}")
    for i, t in enumerate(tables):
        print(f"  [{i}] class={t.get('class')} | id={t.get('id')} | rows={len(t.find_all('tr'))}")

    # Check for any rate-looking numbers in the page
    print(f"\nAll <a> hrefs containing 'idr' or 'gbp':")
    for a in soup.find_all("a", href=True):
        if "idr" in a["href"].lower() or "gbp" in a["href"].lower():
            print(f"  {a['href']} | text={a.get_text(strip=True)}")

    # Check for CAPTCHA / block pages
    body_text = soup.get_text()[:500]
    print(f"\nPage body text (first 500 chars):\n{body_text}")

    # Full HTML dump
    print(f"\nFull HTML (first 3000 chars):\n{driver.page_source[:3000]}")

    driver.quit()

diagnose_year_page()
