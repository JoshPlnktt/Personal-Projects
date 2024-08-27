README.txt

Project: AI Data Scraper for TheresAnAIForThat.com

Description:
This project is designed to scrape data from the website https://theresanaiforthat.com/. It extracts information about AI tools, including titles, descriptions, websites, logos, authors, ratings, primary tasks, tags, and prices. The data is then saved into a CSV file with the current date in the file name.

Requirements:
- Python 3.x
- BeautifulSoup4
- pandas
- datetime
- logging
- ScrapingBee or other scraping client/proxy list (can substitute for requests)

Installation:
1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries using pip.


Usage:
1. Run the script manually whenever you want to scrape the data.
2. The script will save the scraped data into a CSV file with the current date in the file name.

Script Overview:
- `get_proxy(proxy_list)`: Selects a random proxy from the list of proxies.
- `get_html(base_url)`: Retrieves the HTML content of the home page.
- `get_links(soup, base_url)`: Extracts individual product links from the home page HTML.
- `get_description(soup)`: Extracts the description from the HTML.
- `get_tags(soup)`: Extracts the tags from the HTML.
- `get_price(soup)`: Extracts the price from the HTML.
- `get_data(links)`: Processes each link, extracts the required information, and stores it in lists.
- `get_csv(df, csv_name)`: Saves the DataFrame as a CSV file with the current date in the file name.
- `main(base_url)`: Combines all helper functions to navigate from page to page and scrape data.

Logging:
The script uses the logging module to provide detailed information about the progress and any errors encountered. Logs are printed to the console.

Error Handling:
The script includes error handling to manage exceptions and continue processing other links even if one fails.

Example Usage:
1. Run the script: 'main.py'
2. The script will save the scraped data into a CSV file named `ai_list_{current_date}.csv`.

Notes:
- Ensure your scraping client is properly set up. If using ScrapingBee simply enter your API key. 
- The script is designed to be run manually but frequently, so you can update the data as needed.

Author:
Joshua Plunkett

Contact:
Email: joshuaplunkett.data@gmail.com
LinkedIn: www.linkedin.com/in/joshua-plunkett-analytics




