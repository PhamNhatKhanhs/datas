from bs4 import BeautifulSoup

def parse_titles(html):
    """Phân tích tiêu đề bài báo từ trang HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    titles = [title.text.strip() for title in soup.find_all('h3', class_='title-news')]
    return titles
