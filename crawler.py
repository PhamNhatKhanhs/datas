import asyncio
import logging
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import aiohttp

# Import necessary functions from other modules
from fetcher import fetch_home_page, fetch_article_details
from parser import parse_titles, parse_article
from saver import save_to_csv, save_to_json, save_to_database
import config

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log format
    handlers=[
        logging.FileHandler(Path(config.OUTPUT_DIR) / 'crawler.log'),  # Save logs to a file
        logging.StreamHandler()  # Display logs in the console
    ]
)

async def process_article(url, session):
    """
    Process a single article by fetching its content and extracting relevant data.
    
    Args:
        url (str): The URL of the article.
        session (aiohttp.ClientSession): The HTTP session for sending requests.
    
    Returns:
        dict or None: A dictionary containing article details if successful, otherwise None.
    """
    try:
        content = await fetch_article_details(url, session)  # Fetch article content
        if content:
            article_data = parse_article(content)  # Parse article content to extract data
            article_data['url'] = url  # Store the article's URL
            article_data['crawled_at'] = datetime.now().isoformat()  # Store the crawl timestamp
            return article_data  # Return extracted article data
    except Exception as e:
        logging.error(f"Error processing article {url}: {str(e)}")  # Log the error if processing fails
    return None  # Return None if processing fails

async def main():
    """
    The main function for running the web crawler.
    
    - Fetches the homepage and category pages.
    - Extracts article titles and URLs.
    - Processes articles concurrently using asyncio.
    - Saves extracted data in CSV, JSON, and database formats.
    """
    try:
        logging.info("Starting crawler...")  # Log the start of the crawling process
        
        # Fetch and parse homepage
        pages = await fetch_home_page(config.BASE_URL)  # Fetch homepage and category pages
        all_titles = []
        for page in pages:
            titles = parse_titles(page)  # Extract article titles and metadata from each page
            all_titles.extend(titles)  # Store all extracted titles
        
        # Process articles concurrently
        article_data = []
        with tqdm(total=len(all_titles), desc="Processing articles") as pbar:  # Display progress bar
            tasks = []
            async with aiohttp.ClientSession() as session:  # Create a single HTTP session
                for title in all_titles:
                    if 'url' in title:
                        task = asyncio.create_task(process_article(title['url'], session))  # Create async tasks
                        tasks.append(task)
                
                for task in asyncio.as_completed(tasks):  # Process tasks as they complete
                    result = await task
                    if result:
                        article_data.append(result)  # Store the processed article data
                    pbar.update(1)  # Update progress bar
        
        # Save extracted data
        if article_data:
            if config.OUTPUT_FORMAT == "csv":
                save_to_csv(article_data)  # Save data as CSV
            elif config.OUTPUT_FORMAT == "json":
                save_to_json(article_data)  # Save data as JSON
            
            # Always save data to the database
            save_to_database(article_data)
            
            logging.info(f"Successfully crawled {len(article_data)} articles")  # Log success message
        else:
            logging.warning("No articles were crawled")  # Log a warning if no articles were processed
            
    except Exception as e:
        logging.error(f"Crawler failed: {str(e)}")  # Log error if the crawler fails
        raise  # Rethrow the exception for debugging

# Entry point of the program
if __name__ == "__main__":
    asyncio.run(main())  # Run the main function asynchronously
