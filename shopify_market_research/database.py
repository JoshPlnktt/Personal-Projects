"""
This module defines all of the functions that will be used to work with the mysql database. 

All of these functions will be used within main.py to execute the script.
"""

import logging
from mysql import connector
from mysql.connector import Error, IntegrityError


logging.basicConfig(filename='shopify_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def read_config():
    """
    Reads and parses the database login information in the credentials.txt file.

    Arguments:
    - file_path: The file path to the credents.txt file. This project uses a relative path.
    """
    config = {}
    file_path = "config.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config


def open_connection():
    """
    Creates a connection to the database listed in the credentials.txt file. 
    Uses login information provided in the credentials.txt file as well.

    Returns:
    - database: The database connection object
    - cursor: The cursor for accessing and manipulating the database.
    """
    login = read_config()
    try:
        database = connector.connect(
            host=login['host'],
            database=login['database'],
            user=login['user'],
            password=login['password']
        )
        if database.is_connected():
            logging.info(
                "Connected to database: %s. Cursor ready for use.", login['database'])
            cursor = database.cursor()
        return database, cursor
    except Error as e:
        logging.error("Error while connecting to MySQL: %s", e)


def close_connection(db_conn=None, cursor=None):
    """
    Closes the provided database connection and cursor.

    Parameters:
    db_conn (object): The database connection object.
    cursor (object): The cursor object.
    """
    if cursor:
        try:
            cursor.close()
            logging.info("Cursor closed successfully.")
        except connector.Error as err:
            logging.error("Error closing cursor: %s", err)

    if db_conn:
        try:
            db_conn.close()
            logging.info("Database connection closed successfully.")
        except connector.Error as err:
            logging.error("Error closing database connection: %s", err)


def create_tables(cursor, database):
    """
    This function creates the tables for the data to be stored.

    Parameters:
    cursor: The cursor object created with open_connection()
    database: The database connection object
    """
    products_formula = """
    CREATE TABLE IF NOT EXISTS products (
        product_id BIGINT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        vendor VARCHAR(255),
        category VARCHAR(255)
    )
    """
    variants_formula = """
    CREATE TABLE IF NOT EXISTS variants (
        variant_id BIGINT PRIMARY KEY,
        variant_title VARCHAR(255) NOT NULL,
        product_id BIGINT NOT NULL,
        option1 VARCHAR(255),
        option2 VARCHAR(255),
        option3 VARCHAR(255)
    )
    """
    log_formula = """
    CREATE TABLE IF NOT EXISTS log (
        variant_id BIGINT,
        price FLOAT NOT NULL,
        available BOOLEAN,
        date_scraped DATETIME NOT NULL,
        FOREIGN KEY (variant_id) REFERENCES variants(variant_id)
    )
    """

    formulas = [products_formula, variants_formula, log_formula]
    for formula in formulas:
        try:
            cursor.execute(formula)
            database.commit()
            logging.info("Table created or already exists: %s",
                         formula.split()[5])
        except connector.Error as err:
            logging.error(
                "Error creating table with formula: %s - %s", formula, err)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Unexpected error: %s", e)


def upload_data(cursor, database, data):
    """
    Processes the data received from Shopify JSON and uploads it to the database and proper tables.

    Parameters:
    cursor: Your MySQL cursor created with open_connections()
    database: The database connection object
    data (list): A list containing [product_title, product_id, description, vendor, category,
    variant_title, option1, option2, option3, available, price, variant_id, date_scraped]
    """

    product_title, product_id, description, vendor, category, variant_title, option1, option2, option3, available, price, variant_id, date_scraped = data  # pylint: disable=line-too-long

    product_formula = """
    INSERT INTO products (product_id, title, description, vendor, category)
    VALUES (%s, %s, %s, %s, %s)
    """

    variant_formula = """
    INSERT INTO variants (variant_id, variant_title, product_id, option1, option2, option3)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    log_formula = """
    INSERT INTO log (variant_id, price, available, date_scraped)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(product_formula, (product_id,
                       product_title, description, vendor, category))
        database.commit()
        logging.info("New product [%s] added. Product ID: [%s]",
                     product_title, product_id)
    except IntegrityError:
        # No logging needed
        pass
    except connector.Error as err:
        logging.error("Error inserting product into %s table. \nName: [%s], ID: [%s] - [%s]",
                      product_formula.split()[2], product_title, product_id, err)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error: %s", e)

    try:
        cursor.execute(variant_formula, (variant_id, variant_title,
                       product_id, option1, option2, option3))
        database.commit()
        logging.info(
            "New variant [%s] successfully added. Variant ID: [%s]", variant_title, variant_id)
    except IntegrityError:
        # No logging for duplicate variants, just continue
        pass
    except connector.Error as err:
        logging.error("Error inserting variant into %s table. \nName: [%s], ID: [%s] - [%s]",
                      variant_formula.split()[2], variant_title, variant_id, err)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error: %s", e)

    try:
        cursor.execute(
            log_formula, (variant_id, price, available, date_scraped))
        database.commit()
        logging.info(
            "Log entry successfully added for variant. Name: [%s] - ID: [%s]",
            variant_title, variant_id)
    except connector.Error as err:
        logging.error("Error inserting log entry for variant. Name: [%s], ID: [%s] - %s",
                      variant_title, variant_id, err)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error: %s", e)
