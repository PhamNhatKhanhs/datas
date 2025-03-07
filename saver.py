import json
import csv
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict
import pandas as pd
import config

def ensure_output_dir():
    """Đảm bảo thư mục đầu ra tồn tại trước khi lưu file."""
    Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def save_to_csv(data: List[Dict]):
    """Lưu dữ liệu bài viết vào file CSV."""
    try:
        ensure_output_dir()  # Đảm bảo thư mục đầu ra tồn tại
        output_file = Path(config.OUTPUT_DIR) / 'articles.csv'  # Xác định đường dẫn file CSV đầu ra
        
        df = pd.DataFrame(data)  # Chuyển đổi dữ liệu thành DataFrame của Pandas
        df.to_csv(output_file, index=False, encoding='utf-8-sig')  # Lưu thành CSV không có index, đảm bảo hỗ trợ UTF-8
        logging.info(f"Data saved to CSV: {output_file}")  # Ghi log thông báo thành công
        
    except Exception as e:
        logging.error(f"Error saving to CSV: {str(e)}")  # Ghi log lỗi
        raise  # Ném ngoại lệ để gỡ lỗi

def save_to_json(data: List[Dict]):
    """Lưu dữ liệu bài viết vào file JSON."""
    try:
        ensure_output_dir()  # Đảm bảo thư mục đầu ra tồn tại
        output_file = Path(config.OUTPUT_DIR) / 'articles.json'  # Xác định đường dẫn file JSON đầu ra
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # Lưu dữ liệu dạng JSON với mã hóa UTF-8
        logging.info(f"Data saved to JSON: {output_file}")  # Ghi log thông báo thành công
        
    except Exception as e:
        logging.error(f"Error saving to JSON: {str(e)}")  # Ghi log lỗi
        raise  # Ném ngoại lệ để gỡ lỗi

def save_to_database(data: List[Dict]):
    """Lưu dữ liệu bài viết vào cơ sở dữ liệu SQLite."""
    try:
        ensure_output_dir()  # Đảm bảo thư mục đầu ra tồn tại
        db_path = Path(config.OUTPUT_DIR) / 'articles.db'  # Xác định đường dẫn file cơ sở dữ liệu
        
        # Tạo kết nối đến cơ sở dữ liệu SQLite
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Tạo bảng articles nếu chưa tồn tại
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID tự động tăng cho mỗi dòng
                url TEXT UNIQUE,  -- Đảm bảo mỗi URL là duy nhất để tránh trùng lặp
                title TEXT,  -- Tiêu đề của bài viết
                description TEXT,  -- Mô tả ngắn hoặc tóm tắt
                content TEXT,  -- Nội dung đầy đủ của bài viết
                thumbnail TEXT,  -- URL ảnh thumbnail
                publish_time TEXT,  -- Ngày/giờ khi bài viết được xuất bản
                author TEXT,  -- Tác giả của bài viết
                crawled_at TEXT  -- Thời điểm khi bài viết được thu thập
            )
        ''')
        
        # Chèn từng bài viết vào cơ sở dữ liệu, tránh trùng lặp với REPLACE
        for article in data:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (url, title, description, content, thumbnail, publish_time, author, crawled_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('url', ''),  # Lấy URL, mặc định là chuỗi rỗng nếu không có
                article.get('title', ''),  # Lấy tiêu đề
                article.get('description', ''),  # Lấy mô tả
                article.get('content', ''),  # Lấy nội dung
                article.get('thumbnail', ''),  # Lấy URL thumbnail
                article.get('publish_time', ''),  # Lấy thời gian xuất bản
                article.get('author', ''),  # Lấy tên tác giả
                article.get('crawled_at', '')  # Lấy thời điểm thu thập
            ))
        
        conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        conn.close()  # Đóng kết nối cơ sở dữ liệu
        logging.info(f"Data saved to database: {db_path}")  # Ghi log thông báo thành công
        
    except Exception as e:
        logging.error(f"Error saving to database: {str(e)}")  # Ghi log lỗi
        raise  # Ném ngoại lệ để gỡ lỗi
