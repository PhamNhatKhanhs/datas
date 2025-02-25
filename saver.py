import json
import csv
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict
import pandas as pd
import config

def ensure_output_dir():
    """Ensure output directory exists"""
    Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def save_to_csv(data: List[Dict]):
    """Save data to CSV file"""
    try:
        ensure_output_dir()
        output_file = Path(config.OUTPUT_DIR) / 'articles.csv'
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logging.info(f"Data saved to CSV: {output_file}")
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {str(e)}")
        raise

def save_to_json(data: List[Dict]):
    """Save data to JSON file"""
    try:
        ensure_output_dir()
        output_file = Path(config.OUTPUT_DIR) / 'articles.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Data saved to JSON: {output_file}")
        
    except Exception as e:
        logging.error(f"Error saving to JSON: {str(e)}")
        raise

def save_to_database(data: List[Dict]):
    """Save data to SQLite database"""
    try:
        ensure_output_dir()
        db_path = Path(config.OUTPUT_DIR) / 'articles.db'
        
        # Create connection
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                description TEXT,
                content TEXT,
                thumbnail TEXT,
                publish_time TEXT,
                author TEXT,
                crawled_at TEXT
            )
        ''')
        
        # Insert data
        for article in data:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (url, title, description, content, thumbnail, publish_time, author, crawled_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('url', ''),
                article.get('title', ''),
                article.get('description', ''),
                article.get('content', ''),
                article.get('thumbnail', ''),
                article.get('publish_time', ''),
                article.get('author', ''),
                article.get('crawled_at', '')
            ))
        
        conn.commit()
        conn.close()
        logging.info(f"Data saved to database: {db_path}")
        
    except Exception as e:
        logging.error(f"Error saving to database: {str(e)}")
        raise
