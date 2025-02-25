import asyncio
import logging
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import aiohttp

from fetcher import fetch_home_page, fetch_article_details
from parser import parse_titles, parse_article
from saver import save_to_csv, save_to_json, save_to_database
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(config.OUTPUT_DIR) / 'crawler.log'),
        logging.StreamHandler()
    ]
)

async def process_article(url, session):
    """Process a single article URL"""
    try:
        content = await fetch_article_details(url, session)
        if content:
            article_data = parse_article(content)
            article_data['url'] = url
            article_data['crawled_at'] = datetime.now().isoformat()
            return article_data
    except Exception as e:
        logging.error(f"Error processing article {url}: {str(e)}")
    return None

async def main():
    try:
        logging.info("Starting crawler...")
        
        # Fetch and parse home page
        pages = await fetch_home_page(config.BASE_URL)
        all_titles = []
        for page in pages:
            titles = parse_titles(page)
            all_titles.extend(titles)
        
        # Process articles concurrently
        article_data = []
        with tqdm(total=len(all_titles), desc="Processing articles") as pbar:
            tasks = []
            async with aiohttp.ClientSession() as session:
                for title in all_titles:
                    if 'url' in title:
                        task = asyncio.create_task(process_article(title['url'], session))
                        tasks.append(task)
                
                for task in asyncio.as_completed(tasks):
                    result = await task
                    if result:
                        article_data.append(result)
                    pbar.update(1)
        
        # Save data
        if article_data:
            if config.OUTPUT_FORMAT == "csv":
                save_to_csv(article_data)
            elif config.OUTPUT_FORMAT == "json":
                save_to_json(article_data)
            
            # Always save to database
            save_to_database(article_data)
            
            logging.info(f"Successfully crawled {len(article_data)} articles")
        else:
            logging.warning("No articles were crawled")
            
    except Exception as e:
        logging.error(f"Crawler failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
