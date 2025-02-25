from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import re

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_titles(html: str) -> List[Dict]:
    """Parse article titles and metadata from HTML content"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'lxml')
    articles = []
    
    # Find all article elements
    for article in soup.find_all(['article', 'div'], class_=['item-news', 'article-item']):
        try:
            # Find title and link
            title_tag = article.find(['h3', 'h2', 'h1'])
            if not title_tag:
                continue
                
            link_tag = title_tag.find('a')
            if not link_tag:
                continue
                
            # Extract basic info
            title = clean_text(link_tag.get_text())
            url = link_tag.get('href', '')
            if not (title and url):
                continue
            
            # Extract description
            description = ""
            desc_tag = article.find(['p', 'div'], class_=['description', 'lead'])
            if desc_tag:
                description = clean_text(desc_tag.get_text())
            
            # Extract thumbnail
            thumbnail = ""
            img_tag = article.find('img')
            if img_tag:
                thumbnail = img_tag.get('src', img_tag.get('data-src', ''))
            
            articles.append({
                'title': title,
                'url': url,
                'description': description,
                'thumbnail': thumbnail
            })
            
        except Exception as e:
            logging.error(f"Error parsing article: {str(e)}")
            continue
    
    return articles

def parse_article(html: str) -> Optional[Dict]:
    """Parse full article content"""
    if not html:
        return None
        
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        # Get article title
        title = ""
        title_tag = soup.find(['h1', 'h2'], class_=['title-detail', 'title-news'])
        if title_tag:
            title = clean_text(title_tag.get_text())
        
        # Get article description
        description = ""
        desc_tag = soup.find(['p', 'div'], class_=['description', 'lead'])
        if desc_tag:
            description = clean_text(desc_tag.get_text())
        
        # Get article content
        content = ""
        content_tag = soup.find(['article', 'div'], class_=['content-detail', 'article-content'])
        if content_tag:
            # Remove unwanted elements
            for tag in content_tag.find_all(['script', 'style', 'iframe']):
                tag.decompose()
            content = clean_text(content_tag.get_text())
        
        # Get publish time
        publish_time = ""
        time_tag = soup.find(['span', 'div'], class_=['time', 'date'])
        if time_tag:
            publish_time = clean_text(time_tag.get_text())
        
        # Get author
        author = ""
        author_tag = soup.find(['strong', 'div'], class_=['author', 'author_mail'])
        if author_tag:
            author = clean_text(author_tag.get_text())
        
        return {
            'title': title,
            'description': description,
            'content': content,
            'publish_time': publish_time,
            'author': author
        }
        
    except Exception as e:
        logging.error(f"Error parsing article content: {str(e)}")
        return None
