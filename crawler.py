import asyncio
import logging
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import aiohttp

# Nhập các hàm cần thiết từ các module khác
from fetcher import fetch_home_page, fetch_article_details
from parser import parse_titles, parse_article
from saver import save_to_csv, save_to_json, save_to_database
import config

# Thiết lập cấu hình logging
logging.basicConfig(
    level=logging.INFO,  # Đặt mức độ log là INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Định dạng log
    handlers=[
        logging.FileHandler(Path(config.OUTPUT_DIR) / 'crawler.log'),  # Lưu log vào file
        logging.StreamHandler()  # Hiển thị log trên console
    ]
)

async def process_article(url, session):
    """
    Xử lý một bài viết bằng cách tải nội dung và trích xuất dữ liệu liên quan.
    
    Tham số:
        url (str): URL của bài viết.
        session (aiohttp.ClientSession): Phiên HTTP để gửi yêu cầu.
    
    Trả về:
        dict hoặc None: Một từ điển chứa chi tiết bài viết nếu thành công, ngược lại là None.
    """
    try:
        content = await fetch_article_details(url, session)  # Tải nội dung bài viết
        if content:
            article_data = parse_article(content)  # Phân tích nội dung bài viết để trích xuất dữ liệu
            article_data['url'] = url  # Lưu URL của bài viết
            article_data['crawled_at'] = datetime.now().isoformat()  # Lưu thời điểm thu thập
            return article_data  # Trả về dữ liệu bài viết đã trích xuất
    except Exception as e:
        logging.error(f"Lỗi khi xử lý bài viết {url}: {str(e)}")  # Ghi log lỗi nếu xử lý thất bại
    return None  # Trả về None nếu xử lý thất bại

async def main():
    """
    Hàm chính để chạy trình thu thập dữ liệu web.
    
    - Tải trang chủ và các trang chuyên mục.
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
