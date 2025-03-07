from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import re

def clean_text(text: str) -> str:
    """Làm sạch và chuẩn hóa nội dung văn bản bằng cách loại bỏ khoảng trắng thừa."""
    if not text:
        return ""  # Trả về chuỗi rỗng nếu text là None hoặc rỗng
    text = re.sub(r'\s+', ' ', text)  # Thay thế nhiều khoảng trắng bằng một khoảng trắng
    return text.strip()  # Xóa khoảng trắng ở đầu và cuối chuỗi

def parse_titles(html: str) -> List[Dict]:
    """Phân tích các tiêu đề bài viết và metadata từ nội dung HTML."""
    if not html:
        return []  # Trả về danh sách rỗng nếu HTML rỗng
    
    soup = BeautifulSoup(html, 'lxml')  # Phân tích nội dung HTML với trình phân tích lxml
    articles = []  # Danh sách để lưu các bài viết đã trích xuất
    
    # Tìm tất cả các phần tử bài viết chứa tin tức
    for article in soup.find_all(['article', 'div'], class_=['item-news', 'article-item']):
        try:
            # Tìm thẻ tiêu đề (h1, h2, h3)
            title_tag = article.find(['h3', 'h2', 'h1'])
            if not title_tag:
                continue  # Bỏ qua nếu không tìm thấy tiêu đề
                
            # Tìm liên kết trong thẻ tiêu đề
            link_tag = title_tag.find('a')
            if not link_tag:
                continue  # Bỏ qua nếu không tìm thấy liên kết
                
            # Trích xuất văn bản tiêu đề và URL
            title = clean_text(link_tag.get_text())  # Làm sạch tiêu đề đã trích xuất
            url = link_tag.get('href', '')  # Trích xuất URL
            if not (title and url):
                continue  # Bỏ qua nếu thiếu tiêu đề hoặc URL
            
            # Trích xuất mô tả bài viết
            description = ""
            desc_tag = article.find(['p', 'div'], class_=['description', 'lead'])
            if desc_tag:
                description = clean_text(desc_tag.get_text())  # Làm sạch mô tả đã trích xuất
            
            # Trích xuất URL ảnh thumbnail
            thumbnail = ""
            img_tag = article.find('img')
            if img_tag:
                # Lấy nguồn ảnh (src) hoặc sử dụng data-src nếu có
                thumbnail = img_tag.get('src', img_tag.get('data-src', ''))
            
            # Store extracted article details in a dictionary
            articles.append({
                'title': title,
                'url': url,
                'description': description,
                'thumbnail': thumbnail
            })
            
        except Exception as e:
            logging.error(f"Error parsing article: {str(e)}")  # Log error if extraction fails
            continue  # Continue with the next article
    
    return articles  # Return the list of extracted articles

def parse_article(html: str) -> Optional[Dict]:
    """Parse full article content and extract details."""
    if not html:
        return None  # Return None if HTML is empty
        
    try:
        soup = BeautifulSoup(html, 'lxml')  # Parse the HTML content with lxml parser
        
        # Extract the article title
        title = ""
        title_tag = soup.find(['h1', 'h2'], class_=['title-detail', 'title-news'])
        if title_tag:
            title = clean_text(title_tag.get_text())  # Clean extracted title
        
        # Extract article description
        description = ""
        desc_tag = soup.find(['p', 'div'], class_=['description', 'lead'])
        if desc_tag:
            description = clean_text(desc_tag.get_text())  # Clean extracted description
        
        # Extract full article content
        content = ""
        content_tag = soup.find(['article', 'div'], class_=['content-detail', 'article-content'])
        if content_tag:
            # Remove unwanted elements such as scripts, styles, and iframes
            for tag in content_tag.find_all(['script', 'style', 'iframe']):
                tag.decompose()
            content = clean_text(content_tag.get_text())  # Clean extracted content
        
        # Extract publish time of the article
        publish_time = ""
        time_tag = soup.find(['span', 'div'], class_=['time', 'date'])
        if time_tag:
            publish_time = clean_text(time_tag.get_text())  # Clean extracted time
        
        # Extract author information
        author = ""
        author_tag = soup.find(['strong', 'div'], class_=['author', 'author_mail'])
        if author_tag:
            author = clean_text(author_tag.get_text())  # Clean extracted author name
        
        # Return a dictionary containing all extracted article details
        return {
            'title': title,
            'description': description,
            'content': content,
            'publish_time': publish_time,
            'author': author
        }
        
    except Exception as e:
        logging.error(f"Error parsing article content: {str(e)}")  # Log error if extraction fails
        return None  # Return None if an error occurs
