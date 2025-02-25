import aiohttp
import asyncio
import logging
from typing import List, Optional
import config

async def fetch_with_retry(url: str, session: aiohttp.ClientSession, max_retries: int = config.MAX_RETRIES) -> Optional[str]:
    """Fetch URL content with retry mechanism"""
    headers = {'User-Agent': config.USER_AGENT}
    
    for attempt in range(max_retries):
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 404:
                    logging.warning(f"Page not found: {url}")
                    return None
                else:
                    logging.warning(f"HTTP {response.status} for {url}")
        except Exception as e:
            if attempt == max_retries - 1:
                logging.error(f"Failed to fetch {url} after {max_retries} attempts: {str(e)}")
                return None
            await asyncio.sleep(config.RETRY_DELAY * (attempt + 1))
    return None

async def fetch_home_page(base_url: str) -> List[str]:
    """Fetch VnExpress home page and category pages"""
    async with aiohttp.ClientSession() as session:
        # Fetch main page
        content = await fetch_with_retry(base_url, session)
        pages = [content] if content else []
        
        # Fetch category pages (you can add more categories as needed)
        categories = ['thoi-su', 'the-gioi', 'kinh-doanh', 'giai-tri']
        tasks = []
        for category in categories:
            url = f"{base_url}/{category}"
            tasks.append(fetch_with_retry(url, session))
        
        results = await asyncio.gather(*tasks)
        pages.extend([page for page in results if page])
        
        return pages

async def fetch_article_details(url: str, session: aiohttp.ClientSession) -> Optional[str]:
    """Fetch full article content"""
    return await fetch_with_retry(url, session)
