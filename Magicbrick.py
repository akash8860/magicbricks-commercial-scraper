import requests
from bs4 import BeautifulSoup
import pandas as pd
import importlib.util
import os
import re

# Check for openpyxl
def is_openpyxl_available():
    return importlib.util.find_spec("openpyxl") is not None

# Sanitize city name for filename
def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Fetch webpage content
def fetch_webpage(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Scrape one page
def scrape_page(url):
    page = fetch_webpage(url)
    if not page:
        return []

    soup = BeautifulSoup(page, "html.parser")
    main_cards = soup.find_all('div', class_='mb-srp__card')
    all_card_data = []

    for card in main_cards:
        card_data = {}

        # Property Name
        try:
            card_data['Property Name'] = card.find('h2', class_='mb-srp__card--title').get_text(strip=True)
        except:
            card_data['Property Name'] = None

        # Summary Details
        try:
            summary_list = card.find_all('div', class_='mb-srp__card__summary__list--item')
            for item in summary_list:
                label = item.find('div', class_='mb-srp__card__summary--label')
                value = item.find('div', class_='mb-srp__card__summary--value')
                if label and value:
                    key = item.get('data-summary', label.get_text(strip=True))
                    card_data[key] = value.get_text(strip=True)
        except:
            pass

        # Price Info
        try:
            price_block = card.find('div', class_='mb-srp__card__estimate')
            card_data['Total Price'] = price_block.find('div', class_='mb-srp__card__price--amount').get_text(strip=True)
            price_per_sqft = price_block.find('div', class_='mb-srp__card__price--size')
            card_data['Price per Sqft'] = price_per_sqft.get_text(strip=True) if price_per_sqft else None
        except:
            card_data['Total Price'] = None
            card_data['Price per Sqft'] = None

        all_card_data.append(card_data)

    return all_card_data

# Scrape multiple pages
def scrape_multiple_pages(base_url, num_pages):
    all_results = []
    for page in range(1, num_pages + 1):
        full_url = f"{base_url}&page={page}"
        print(f"🔄 Scraping page {page}...")
        page_data = scrape_page(full_url)
        if not page_data:
            print(f"❌ No data on page {page}. Stopping early.")
            break
        all_results.extend(page_data)
    return all_results

# Main Execution
if __name__ == "__main__":
    if not is_openpyxl_available():
        print("❌ openpyxl is not installed. Please install it using: pip install openpyxl")
    else:
        cities = [
            "New-Delhi","Mumbai","Kolkata","Chennai","Bengaluru","Hyderabad","Ahmedabad","Pune","Lucknow","Jaipur","Kochi","Nagpur","Noida","Kanpur","Navi-Mumbai","Bhopal","Indore","Surat","Patna","Meerut","Greater-Noida"
        ]

        base_url_template = "https://www.magicbricks.com/property-for-rent/commercial-real-estate?proptype=Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/-Godown,Industrial-Building,Industrial-Shed&cityName={}"
        num_pages = 2400
        # Define the save directory
        save_dir = r"D:\Residential Sell"   
        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)
        for city in cities:
            print(f"\n🏙️ Now scraping city: {city}")
            formatted_city = city.replace(" ", "%20")  # Proper URL encoding
            city_url = base_url_template.format(formatted_city)

            # Scrape data
            city_data = scrape_multiple_pages(city_url, num_pages)

            if city_data:
                df = pd.DataFrame(city_data)
                filename = f"{sanitize_filename(city)}_Properties.xlsx"
                df.to_excel(filename, index=False)
                print(f"✅ Saved {len(df)} records for {city} → {filename}")
            else:
                print(f"⚠️ No data collected for {city}")
