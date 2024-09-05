"""
This module scrapes the product data from the shopify stores.

Using links found in the urls.txt file, it retrieves and parses the product data.
Then, using functions from database.py, the bot will upload the data to a relational database.

To understand how to use the bot, examine the README.txt file before proceeding.
"""

import logging
from datetime import datetime
import time
from scrapingbee import ScrapingBeeClient
import orjson
from bs4 import BeautifulSoup
from database import open_connection, close_connection, create_tables, upload_data, read_config


logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def read_urls():
    """
    This function reads and parses the urls listed in urls.txt

    Parameters:
    - None: Simply list the desired urls in urls.txt
    Returns:
    - urls: A list of the urls parsed from urls.txt
    """
    urls = []
    file_path = "urls.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            urls.append(line.strip())
    logging.info("URLS parsed and ready for use. URL count: %s", len(urls))
    return urls


def get_json(url):
    """
    Retrieves the JSON data found in the shopify store URL. Used in combination with read_urls()

    Parameters:
    - url: The URL to the shopify store you would like to scrape

    Returns:
    - json_data: An object with the products.json data of the shopify store
    """
    login = read_config()
    key = login['api_key']
    client = ScrapingBeeClient(api_key=key)
    try:
        resp = client.get(url)
        resp.raise_for_status()
        json_data = orjson.loads(resp.text)  # pylint: disable=no-member
        return json_data
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Failed to fetch data from %s: %s", url, e)


def parse_and_upload(json_data, cursor, database):
    """
    Parses and uploads to database the json data retrieved with get_json().

    Parameters:
    - json_data: The json data to be parsed
    - cursor: Your MySQL cursor object
    - database: Your MySQL database connection object
    """
    if json_data:
        for product in json_data.get('products', []):
            product_title = product.get('title')
            product_id = product.get('id')
            body_html = product.get('body_html')
            if body_html:
                description = BeautifulSoup(
                    body_html, 'html.parser').get_text().strip()
            else:
                logging.error(
                    "Product with ID [%s] has no body_html. Skipping this product.", product_id)
                continue
            vendor = product.get('vendor')
            category = product.get('product_type')
            for variant in product.get('variants', []):
                variant_title = variant.get('title', 'Default Title')
                if variant_title == 'Default Title':
                    variant_title = product_title

                option1 = variant.get('option1')
                option2 = variant.get('option2')
                option3 = variant.get('option3')
                options = [option1, option2, option3]
                for i, option in enumerate(options):
                    if option == "Default Title":
                        options[i] = variant_title
                option1, option2, option3 = options
                available = variant.get('available')
                price = variant.get('price')
                variant_id = variant.get('id')
                current_datetime = datetime.now()
                date_scraped = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                data = [product_title, product_id, description, vendor, category, variant_title,
                        option1, option2, option3, available, price, variant_id, date_scraped]
                upload_data(cursor, database, data)
    else:
        logging.info("Error with current URL. Proceeding to next provided URL")


def main():
    """
    Combines all functions to scrape, parse, and upload product data from shopify stores.
    """
    start_time = time.time()
    database, cursor = open_connection()
    create_tables(cursor=cursor, database=database)
    urls = read_urls()
    total_urls = len(urls)
    good_urls = 0
    bad_urls = 0
    for base_url in urls:
        products_url = base_url + "products.json"
        data = get_json(products_url)
        if data:
            logging.info("Successfully retrieved data from: %s", products_url)
            parse_and_upload(json_data=data, cursor=cursor, database=database)
            good_urls += 1
        else:
            logging.info("Skipping %s due to an error.", products_url)
            bad_urls += 1
    close_connection(db_conn=database, cursor=cursor)
    end_time = time.time()
    total_time = end_time - start_time
    logging.info("""\nTotal URLS provided: %s,
Success count: %s, \nFailure count: %s, \nOverall success rate: %s, \nTotal run time: %s""",
                 total_urls, good_urls, bad_urls,
                 f"{round(good_urls / total_urls * 100, 2)}%", f"{round(total_time / 60, 2)} mins.")


if __name__ == "__main__":
    main()
