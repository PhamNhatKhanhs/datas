import aiohttp
import asyncio
import logging
from typing import List, Optional
import config

async def fetch_with_retry(url: str, session: aiohttp.ClientSession, max_retries: int = config.MAX_RETRIES) -> Optional[str]:
    """Fetch URL content with retry mechanism."""
    headers = {'User-Agent': config.USER_AGENT}  # Set custom User-Agent to mimic a browser
    
    for attempt in range(max_retries):  # Retry up to max_retries times
        try:
            async with session.get(url, headers=headers) as response:  # Send an async GET request
                if response.status == 200:
                    return await response.text()  # Return page content if successful
                elif response.status == 404:
                    logging.warning(f"Page not found: {url}")  # Log a warning if page is not found
                    return None
                else:
                    logging.warning(f"HTTP {response.status} for {url}")  # Log unexpected HTTP status codes
        except Exception as e:
            if attempt == max_retries - 1:
                logging.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")  # Log error after max retries
                return None
            await asyncio.sleep(config.RETRY_DELAY * (attempt + 1))  # Wait before retrying, increasing delay each attempt
    return None  # Return None if all attempts fail

async def fetch_home_page(base_url: str) -> List[str]:
    """Fetch VnExpress home page and category pages."""
    async with aiohttp.ClientSession() as session:  # Create an HTTP session for efficient connection reuse
        # Fetch main home page
        content = await fetch_with_retry(base_url, session)
        pages = [content] if content else []  # Store main page content if successful
        
        # List of category pages to fetch
        categories = ['thoi-su', 'the-gioi', 'kinh-doanh', 'giai-tri']  # List of categories to scrape
        tasks = []  # List to store async tasks
        
        for category in categories:
            url = f"{base_url}/{category}"  # Construct category URL
            tasks.append(fetch_with_retry(url, session))  # Add fetch task for each category
        
        results = await asyncio.gather(*tasks)  # Execute all tasks concurrently
        pages.extend([page for page in results if page])  # Add successful category pages to the list
        
        return pages  # Return list of fetched pages

async def fetch_article_details(url: str, session: aiohttp.ClientSession) -> Optional[str]:
    """Fetch full article content from the given URL."""
    return await fetch_with_retry(url, session)  # Reuse fetch_with_retry function to get article content
