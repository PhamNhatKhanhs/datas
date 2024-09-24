# pham-nhat-khanh-data-crawler
# Báo cáo Tìm hiểu Crawler Data

## 1. Giới thiệu
**Web Crawler** là một chương trình tự động được thiết kế để duyệt và thu thập dữ liệu từ các trang web. Nó có thể được sử dụng để trích xuất các thông tin như bài báo, sản phẩm, đánh giá, hoặc bất kỳ nội dung nào có sẵn trên các trang web. Mục tiêu của chúng tôi là xây dựng một chương trình Crawler để thu thập dữ liệu từ trang VnExpress và lưu lại các thông tin đã thu thập dưới định dạng file (CSV, JSON) hoặc cơ sở dữ liệu quan hệ (MySQL, PostgreSQL).

Trong bài báo cáo này, chúng tôi sẽ trình bày quá trình tìm hiểu và triển khai một chương trình crawler cơ bản, sử dụng ngôn ngữ Python và các thư viện hỗ trợ như `requests`, `BeautifulSoup` để thu thập và xử lý dữ liệu.

---

## 2. Công nghệ sử dụng
Dưới đây là các công nghệ và công cụ mà nhóm đã sử dụng để thực hiện bài tập này:

### 2.1. Ngôn ngữ lập trình:
- **Python 3**: Một ngôn ngữ lập trình mạnh mẽ, dễ học và có nhiều thư viện hỗ trợ cho việc thu thập và xử lý dữ liệu.

### 2.2. Thư viện Python:
- **`requests`**: Được sử dụng để gửi các yêu cầu HTTP đến các trang web, từ đó tải về nội dung HTML.
- **`BeautifulSoup`**: Thư viện để phân tích và trích xuất dữ liệu từ các trang HTML.
- **`json`**: Để xử lý dữ liệu ở định dạng JSON.

### 2.3. Các công cụ khác:
- **Docker**: Để đóng gói và triển khai chương trình crawler trong môi trường container hóa.
- **Docker Compose**: Để dễ dàng quản lý các container khi triển khai nhiều dịch vụ cùng lúc.

---

## 3. Quá trình thực hiện

### 3.1. Bước 1: Cấu trúc chương trình

Chương trình crawler được xây dựng theo các bước cơ bản như sau:
1. **Gửi yêu cầu HTTP**: Sử dụng thư viện `requests` để gửi yêu cầu GET đến các trang web cần thu thập dữ liệu.
2. **Phân tích HTML**: Dùng `BeautifulSoup` để phân tích cấu trúc HTML và trích xuất thông tin cần thiết (tiêu đề bài viết, link, mô tả, hình ảnh).
3. **Lưu trữ dữ liệu**: Dữ liệu sau khi thu thập được lưu vào file dưới các định dạng CSV và JSON.

### 3.2. Bước 2: Viết mã nguồn

#### 3.2.1. Crawler cơ bản

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def fetch_data_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối đến {url}: {e}")
        return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='item-news')
    data = []
    
    for article in articles:
        title = article.h3.a.text.strip()
        link = article.h3.a['href']
        description = article.p.text.strip() if article.p else 'N/A'
        img = article.img['src'] if article.img else 'N/A'
        data.append({
            'title': title,
            'link': link,
            'description': description,
            'img': img
        })
    
    return data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

base_url = "https://vnexpress.net/"
html_content = fetch_data_from_page(base_url)

if html_content:
    extracted_data = parse_html(html_content)
    save_to_csv(extracted_data, 'vnexpress_data.csv')
    save_to_json(extracted_data, 'vnexpress_data.json')
    print("Dữ liệu đã được lưu dưới dạng CSV và JSON.")
else:
    print("Không thể lấy dữ liệu từ trang web.")

Để triển khai ứng dụng này bằng Docker, chúng tôi đã tạo một file Dockerfile như sau:

# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "crawler.py"]
Chúng tôi cũng sử dụng Docker Compose để dễ dàng quản lý và triển khai ứng dụng:

yaml
# docker-compose.yml
version: '3.8'

services:
  crawler:
    build: .
    volumes:
      - ./output:/app/output

3.3. Chạy Ứng Dụng
Để chạy ứng dụng với Docker, hãy sử dụng các lệnh sau:

Xây dựng hình ảnh Docker:
docker build -t data-crawler .

Chạy container:
docker run -it -v $(pwd)/output:/app/output data-crawler
