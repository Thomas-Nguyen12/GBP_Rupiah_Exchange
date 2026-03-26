from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_exchange_rates_selenium(from_currency: str, to_currency: str):
    """
    Scrape historical exchange rate data directly from page HTML (no iframe).
    Automatically detects all available years and returns a pandas DataFrame.
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
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

    print(f"Loading: {base_url}")
    driver.get(base_url)
    time.sleep(4)

    # -------------------------
    # Extract available years
    # -------------------------
    # Wait for year links to appear anywhere on the page
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='exchange-rate-history']"))
        )
    except Exception:
        driver.quit()
        raise RuntimeError(
            "Could not find year navigation links. "
            "The site structure may have changed again."
        )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all links that look like year selectors (4-digit year text)
    available_years = []
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        if text.isdigit() and len(text) == 4:
            available_years.append(int(text))

    # Deduplicate and sort
    available_years = sorted(set(available_years), reverse=True)

    if not available_years:
        # Fallback: dump page snippet to help diagnose
        print("No year links found. Page snippet:")
        print(driver.page_source[:3000])
        driver.quit()
        raise ValueError("No year links found — site structure may have changed.")

    print(f"Detected years: {available_years}")

    all_rows = []

    # -------------------------
    # Loop through each year
    # -------------------------
    for year in available_years:
        print(f"Scraping year {year}...")
        year_url = (
            f"https://www.exchange-rates.org/exchange-rate-history/"
            f"{from_currency.lower()}-{to_currency.lower()}/{year}"
        )

        try:
            driver.get(year_url)

            # Wait for the data table to appear
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Try to find any table with date/rate data
            table = soup.select_one("table")
            if table is None:
                print(f"  No table found for {year}, skipping.")
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
            print(f"  Error scraping {year}: {e} — skipping.")
            continue

    driver.quit()

    if not all_rows:
        raise RuntimeError("No data collected. The table structure may have changed.")

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
print(f"\nTotal rows: {len(data)}")
print(f"Date range: {data['Date'].min()} → {data['Date'].max()}")


data.to_csv("data/all_data.csv")