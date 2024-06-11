import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import psycopg2
import logging
from db_config import DB_HOST, DB_NAME, DB_USER, DB_PASS

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='scraper.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define headers to simulate a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Base URL of the Amazon search 
BASE_URL = input('Enter URL of Amazon search: ') 

# Function to connect to the database
def connect_db():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return None

# Function to save data to the database
def save_to_db(data, conn):
    try:
        with conn.cursor() as cur:
            for item in data:
                cur.execute("""
                    INSERT INTO scraperdata(name, price, rating, reviews, url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (item['name'], item['price'], item['rating'], item['reviews'], item['url']))
        conn.commit()
    except Exception as e:
        logging.error(f"Error saving data to database: {e}")
        conn.rollback()

# Function to extract data from a single page
def extract_data(page_number):
    try:
        url = f"{BASE_URL}{page_number}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all product listings on the page
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        data = []
        for product in products:
            name = product.h2.text.strip()
            price = product.find("span", "a-price-whole")  # Adjusted to capture the whole price element
            rating = product.find("span", {"class": "a-icon-alt"})
            reviews = product.find("span", {"class": "a-size-base"})
            product_url = "https://www.amazon.in" + product.h2.a['href']

            # Only capture the text of the first price element
            price_text = price.text.strip() if price else None

            data.append({
                "name": name,
                "price": '₹'+price_text,
                "rating": rating.text.strip() if rating else None,
                "reviews": reviews.text.strip() if reviews else None,
                "url": product_url
            })
        return data
    except Exception as e:
        logging.error(f"Error extracting data from page {page_number}: {e}")
        return []


# Function to handle threading
def scrape_amazon(num_pages):
    all_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_page = {executor.submit(extract_data, page): page for page in range(1, num_pages + 1)}
        for future in future_to_page:
            try:
                data = future.result()
                all_data.extend(data)
                logging.info(f"Successfully scraped page {future_to_page[future]}")
            except Exception as e:
                logging.error(f"Error processing page {future_to_page[future]}: {e}")
    return all_data

# Main function to start the scraping process
if __name__ == "__main__":
    num_pages = 5 #Number of pages to scrape 
    logging.info(f"Starting scraping for {num_pages} pages")

    conn = connect_db()
    if conn:
        scraped_data = scrape_amazon(num_pages)
        save_to_db(scraped_data, conn)
        conn.close()
        logging.info("Scraping and saving process completed successfully")
    else:
        logging.error("Failed to connect to the database. Exiting.")
