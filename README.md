# Amazon Scraper

## Overview
This repository contains a Python script designed to scrape product data from Amazon and store it in a PostgreSQL database. The script uses threading for efficient data extraction and logs all operations for monitoring and debugging purposes.

## Features
- Scrapes product name, price, rating, number of reviews, and URL.
- Utilizes multi-threading to scrape multiple pages concurrently.
- Stores data in a PostgreSQL database.
- Comprehensive logging for error tracking and process monitoring.

## Requirements
- Python 3.x
- Packages: `requests`, `beautifulsoup4`, `psycopg2`
- PostgreSQL database
- `db_config.py` file for database credentials

## Setup

### Install Packages
Install the necessary Python packages:
```sh
pip install requests beautifulsoup4 psycopg2
```

### Database Configuration
Create a `db_config.py` file in the root directory with your database credentials:
```python
DB_HOST = 'your_db_host'
DB_NAME = 'your_db_name'
DB_USER = 'your_db_user'
DB_PASS = 'your_db_password'
```

### Database Schema
Ensure your PostgreSQL database has the following table:
```sql
CREATE TABLE scraperdata (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price TEXT,
    rating TEXT,
    reviews TEXT,
    url TEXT
);
```

### Usage

1. **Enter Amazon Search URL**: The script will prompt you to input the base URL.
2. **Run the Script**: Execute the script with Python:
   ```sh
   python scraper.py
   ```
3. **Check Logs**: Review `scraper.log` for detailed logs.

## Functionality

### Connecting to the Database
The script connects to the PostgreSQL database using credentials from `db_config.py`. If the connection fails, it logs the error and exits.

### Data Extraction
The script scrapes product data from specified Amazon search result pages. It captures product name, price, rating, number of reviews, and URL.

### Saving Data to Database
Scraped data is saved into the PostgreSQL database. If an error occurs during this process, it is logged, and the transaction is rolled back.

### Multi-threading
To speed up the scraping process, the script uses threading to scrape multiple pages concurrently.

### Logging
All operations and errors are logged into `scraper.log`, which helps in monitoring the scraping process and troubleshooting issues.

## Example
1. **Run the script**: After setting up, execute the script.
2. **Monitor Progress**: Check `scraper.log` to ensure data is being scraped and saved correctly.
3. **Database**: Verify that the data appears in your PostgreSQL database as expected.

## Repository Structure
```
├── README.md
├── db_config.py
├── scraper.py
└── scraper.log
```

