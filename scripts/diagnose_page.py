from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_exchange_rates_selenium(from_currency: str, to_currency: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Spoof a real user-agent to reduce bot detection
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    base_url = (
        f"https://www.exchange-rates.org/exchange-rate-history/"
        f"{from_currency.lower()}-{to_currency.lower()}"
    )
    driver.get(base_url)
    time.sleep(4)  # Allow JS/redirects to settle

    # -------------------------
    # Locate the iframe flexibly
    # -------------------------
    # Try known ID first, then fall back to any iframe present
    iframe = None
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_M_iframe"))
        )
        print("Found iframe by ID: ctl00_M_iframe")
    except Exception:
        print("ctl00_M_iframe not found — scanning for any iframe...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if not iframes:
            driver.quit()
            raise RuntimeError(
                "No iframes found on page. "
                "The site may have changed structure or is blocking the request.\n"
                f"Page title: {driver.title}"
            )
        # Use the first iframe as best guess; adjust index if needed
        iframe = iframes[0]
        print(f"Falling back to first iframe found: id={iframe.get_attribute('id')}")

    driver.switch_to.frame(iframe)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(2)

    # -------------------------
    # Extract available years
    # -------------------------
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ctl00_M_lblYears"))
        )
    except Exception:
        # Dump iframe HTML to help diagnose structure changes
        print("Could not find #ctl00_M_lblYears. Iframe HTML snippet:")
        print(driver.page_source[:3000])
        driver.quit()
        raise RuntimeError("Year selector not found inside iframe.")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    year_links = soup.select("#ctl00_M_lblYears a")

    available_years = []
    for a in year_links:
        text = a.get_text(strip=True)
        if text.isdigit() and len(text) == 4:
            available_years.append(int(text))

    if not available_years:
        driver.quit()
        raise ValueError("No year links found — iframe structure may have changed.")

    years_to_fetch = sorted(available_years, reverse=True)
    print(f"Detected years: {years_to_fetch}")

    all_rows = []

    # -------------------------
    # Loop through each year
    # -------------------------
    for year in years_to_fetch:
        print(f"Scraping year {year}...")
        try:
            year_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, str(year)))
            )
            year_link.click()

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
            )
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.select_one("table.table")

            if table is None:
                print(f"  Warning: no table found for {year}, skipping.")
                continue

            for row in table.select("tbody tr"):
                cols = [c.get_text(strip=True) for c in row.select("td")]
                if len(cols) >= 2:
                    try:
                        all_rows.append({
                            "Date": cols[0],
                            "Rate": float(cols[1].replace(",", "")),
                            "From": from_currency.upper(),
                            "To": to_currency.upper(),
                        })
                    except ValueError:
                        print(f"  Skipping unparseable row: {cols}")

        except Exception as e:
            print(f"  Error scraping year {year}: {e} — skipping.")
            continue

    driver.quit()

    if not all_rows:
        raise RuntimeError("No data collected. Check diagnostic output above.")

    # -------------------------
    # Convert to DataFrame
    # -------------------------
    df = pd.DataFrame(all_rows)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


data = get_exchange_rates_selenium("IDR", "GBP")
print(data)
