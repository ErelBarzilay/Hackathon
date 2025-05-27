import platform
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL of the webpage to scrape
RESOURCE_IDS = {
    "population": "residents_in_israel_by_communities_and_age_groups/resource/64edd0ee-3d5d-43ce-8562-c336c24dbc1f", 
    "bus": "bus_rishui_bitzua_2021/resource/86eceab6-44ac-4301-a6a7-9a4a92dae48b", 
    "train": "train_trip/resource/6cf35ec2-c0eb-4ef0-a904-f093dab0abfd"
    }

def get_last_update(driver, resource_id, *args):

    url = f"https://data.gov.il/dataset/{resource_id}"
    driver.get(url)

    # Wait for the table to be present in the DOM
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        print("Page loaded successfully.")
    except Exception as e:
        print(f"Error loading table for {resource_id}: {e}")
        return

    # Grab the HTML after the page has loaded
    html = driver.page_source

    # Assuming 'html' contains your HTML string
    soup = BeautifulSoup(html.lower(), "html.parser")

    # Find the table
    table = soup.find("table", class_="table-striped")

    # Create a dictionary for the data
    data_dict = {}

    # Loop through each row in the tbody
    for row in table.find("tbody").find_all("tr"):
        key_tag = row.find("th")
        value_tag = row.find("td")
        
        if key_tag and value_tag:
            key = key_tag.get_text(separator=" ", strip=True)
            
            # Get all <p> tags in the <td>
            p_tags = value_tag.find_all("p")
            
            # Start from the second <p> element (index 1)
            value = " ".join(p.get_text(strip=True) for p in p_tags[1:])
            
            data_dict[key] = value

    # Print the parsed key-value pairs
    for key, value in data_dict.items():
        if "last updated" in key.lower():
            cleaned_value = value.replace("\n", "").replace("|", "").replace("  ", "").strip()
            try:
                return datetime.strptime(cleaned_value, "%d %b %Y %H:%M")
            except Exception as e:
                print(f"Error parsing {cleaned_value} with {e}")
                return cleaned_value

def open_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Helpful for Windows headless
    options.add_argument("--no-sandbox")   # Needed in some Linux containers
    options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in Docker

    # Set user-agent (optional)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.6778.140 Safari/537.36"
    )

    # Detect platform to adjust paths
    if platform.system() == "Linux":
        # Docker/Linux paths
        options.binary_location = "/usr/bin/chromium"
        service = Service(executable_path="/usr/bin/chromedriver")
    else:
        # On Windows, just assume Chrome and ChromeDriver are in PATH
        service = Service()  # Will use default system PATH

    return webdriver.Chrome(service=service, options=options)

def set_cookies(driver):
    # Set cookies to access the site
    driver.get("https://data.gov.il")  # Visit domain to allow setting cookies
    driver.add_cookie({
        'name': 'ckan',
        'value': '59f15554713ea5891cafe62654ebcca493feab1fgAJ9cQAoWAcAAABfZG9tYWlucQFOWAUAAABfcGF0aHECWAEAAAAvcQNYAwAAAF9pZHEEWCAAAABkZmRlYmQ5ZjU5NWU0ZmI1OWU1MjlmYTY0MjlhNzc1NXEFWAYAAABfZnJlc2hxBolYDgAAAF9jcmVhdGlvbl90aW1lcQdHQdoNJ5iN9nVYDgAAAF9hY2Nlc3NlZF90aW1lcQhHQdoNJ5iN9nl1Lg=='
    })
    driver.add_cookie({
        'name': 'rbzid',
        'value': 'thyG/xae0kueZ+/N8/fWY/AzoqC0Tz+zhOSjbRE+ED9nIEQurN/9rG6sgRm7mR1fNWPqCgjOy/rRi3Ffxw/hU/C/wj0xnMa78fwTXfUl6rM/O09z5EIOuTNhODTtiuy+sG0nB4/MlGBpDUtvTmwCjFL6bBDe8ZlxLtvNz2M/8N23ymMCVUTOzAztmOK4vRQXdJxCZLKHPtuscThWb2iFVjuqs67bWn0XH25uRgPapd9FTgC7ukkLC/fZN7zJoLrRcN6S6jNM+Wy17A5jRgxEmw=='
    })
    driver.add_cookie({
        'name': 'rbzsessionid',
        'value': 'b4b3803ad108702fa76f228a156dbcbe'
    })
    return driver

def quit_driver(driver):
    if driver:
        driver.quit()

def scrape_data(driver, resource_name):
    print(f"Scraping data for resource: {resource_name}")
    resource_id = RESOURCE_IDS.get(resource_name)
    print(f"Resource ID: {resource_id}")
    if not resource_id:
        print(f"Resource ID for {resource_name} not found.")
        return
    return get_last_update(driver, resource_id)


# def main():
#     driver = open_driver()
#     driver = set_cookies(driver)

#     for resource_name in RESOURCE_IDS:
#         scrape_data(driver, resource_name)

#     quit_driver(driver)

# if __name__ == "__main__":
#     main()