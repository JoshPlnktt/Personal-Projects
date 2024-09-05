# Shopify Product Data Scraper


## Project Description
This Python project scrapes product data from Shopify stores and uploads the data into a MySQL database.

The script retrieves product information such as title, description, vendor, category, variants, and pricing details from the
shopify store's 'product.json' endpoint.

The purpose is to serve as a market research tool. This allows you to automate data collection for things like competitor analysis, pricing analysis, and more.


## Prerequisites
- Python 3.x
- MySQL database
- ScrapingBee subscription or other proxy management tool.
- Required packages:
    - 'scrapingbee': Used to handle requests and bypass bot protection
    - 'mysql-connector-python': Used to access and manipulate your SQL database
    - 'orjson': Used to parse and extract JSON data
    - 'bs4': Used to parse HTML code to extract product descriptions

The file comes with a virtual environment, to ensure all dependencies are met.


## Installation
1. Clone the repository or downloaded the project folder

2. Install the required Python packages: 
    - pip install scrapingbee mysql-connector-python orjson bs4

3. Set up your MySQL server, and create a database you would like your tables/data to be stored in.


## Configuration
To configure the script to your MySQL database and ScrapingBee client, you will use the config.txt file.

1. Set up your database
    - To set up your database, enter the corresponding MySQL data to the config.txt file. Ensure to add no extra spaces or quotation marks, with each entry on its own line.
        - Ex. user=root
    - You do NOT need to create the tables for the data, the script with run a 'CREATE TABLE IF NOT EXISTS' logical check everytime the script is run.

2. Set up your request client.
    - I like to use scrapingbee. If you also have scrapingbee, you can enter your API key into the config.txt file as well.
    - If you do not have scrapingbee, you can make simple adjustments to the get_json() function in main.py to choose a different client or proxy manager.


## Usage
1. Add the shopify stores you would like to scrape to the urls.txt file, with one URL per line. There are a few example URLS in the list for reference.
    - You can add or remove URLS at any time
    - It must be the sites plain url, not the /products.json/ endpoint.
        - Ex. https://www.tentree.com/

2. Run the main script: main.py

3. The script will scrape the product data from each Shopify store URL and upload the data into the MySQL database in 3 seperate tables.


## Logging
The script uses the logging module to log messages. The log messages are saved to the app.log file for debuging and review.
When the script finished running it will list in the log: how many links you listed, how many were successful/failed, the success rate, and run time.


## Error handling
If the products.json endpoint is not accessible or the JSON data is invalid, the script will log an error message and move on to the next URL.


## Data Model 
The script will create (if the table does not exist in the listed database) the tables used for storing the data. These tables are:
- products: A table with all of the unique products
- variants: A table with all of the unique variants of said products
- log: A table with the variant id, price, availability, and the datetime the data was scraped.

If a product was already added, next time you run the script it will not add it again. It will only add an entry to the log.

Once the script has run, feel free to explore the MySQL tables to better understand the value of these 3 tables.


### Contact
For any questions or issues, please feel free to contact me at: joshuaplunkett.data@gmail.com
