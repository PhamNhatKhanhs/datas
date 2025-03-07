import json
import csv
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict
import pandas as pd
import config

def ensure_output_dir():
    """Ensure that the output directory exists before saving files."""
    Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def save_to_csv(data: List[Dict]):
    """Save article data to a CSV file."""
    try:
        ensure_output_dir()  # Ensure the output directory exists
        output_file = Path(config.OUTPUT_DIR) / 'articles.csv'  # Define the output CSV file path
        
        df = pd.DataFrame(data)  # Convert data to a Pandas DataFrame
        df.to_csv(output_file, index=False, encoding='utf-8-sig')  # Save as CSV without an index, ensuring UTF-8 support
        logging.info(f"Data saved to CSV: {output_file}")  # Log success message
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {str(e)}")  # Log any errors
        raise  # Raise the exception for debugging

def save_to_json(data: List[Dict]):
    """Save article data to a JSON file."""
    try:
        ensure_output_dir()  # Ensure the output directory exists
        output_file = Path(config.OUTPUT_DIR) / 'articles.json'  # Define the output JSON file path
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # Save data in JSON format with UTF-8 encoding
        logging.info(f"Data saved to JSON: {output_file}")  # Log success message
        
    except Exception as e:
        logging.error(f"Error saving to JSON: {str(e)}")  # Log any errors
        raise  # Raise the exception for debugging

def save_to_database(data: List[Dict]):
    """Save article data to an SQLite database."""
    try:
        ensure_output_dir()  # Ensure the output directory exists
        db_path = Path(config.OUTPUT_DIR) / 'articles.db'  # Define the database file path
        
        # Create a connection to the SQLite database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create the articles table if it does not already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-increment ID for each row
                url TEXT UNIQUE,  -- Ensure each URL is unique to avoid duplicates
                title TEXT,  -- Title of the article
                description TEXT,  -- Short description or summary
                content TEXT,  -- Full article content
                thumbnail TEXT,  -- Thumbnail image URL
                publish_time TEXT,  -- Date/time when the article was published
                author TEXT,  -- Author of the article
                crawled_at TEXT  -- Timestamp when the article was crawled
            )
        ''')
        
        # Insert each article into the database, avoiding duplicates with REPLACE
        for article in data:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (url, title, description, content, thumbnail, publish_time, author, crawled_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('url', ''),  # Retrieve URL, default to empty string if missing
                article.get('title', ''),  # Retrieve title
                article.get('description', ''),  # Retrieve description
                article.get('content', ''),  # Retrieve content
                article.get('thumbnail', ''),  # Retrieve thumbnail URL
                article.get('publish_time', ''),  # Retrieve publish time
                article.get('author', ''),  # Retrieve author name
                article.get('crawled_at', '')  # Retrieve crawl timestamp
            ))
        
        conn.commit()  # Save changes to the database
        conn.close()  # Close the database connection
        logging.info(f"Data saved to database: {db_path}")  # Log success message
        
    except Exception as e:
        logging.error(f"Error saving to database: {str(e)}")  # Log any errors
        raise  # Raise the exception for debugging
