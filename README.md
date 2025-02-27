# Dự Án Crawler VnExpress

## 1. Tổng Quan

### 1.1. Giới Thiệu về VnExpress
VnExpress là một trong những trang báo điện tử hàng đầu tại Việt Nam, được thành lập vào năm 2001 bởi FPT Group. Với hơn 20 năm hoạt động, VnExpress đã trở thành nguồn thông tin tin cậy với:

- **Độc giả**: Hơn 40 triệu lượt truy cập hàng tháng
- **Nội dung**: Cập nhật 24/7 với hơn 1,000 tin bài mỗi ngày
- **Chuyên mục**: Đa dạng từ thời sự, kinh doanh, thế giới đến giải trí, thể thao
- **Chất lượng**: Thông tin chính thống, được kiểm chứng kỹ lưỡng
- **Tương tác**: Hệ thống bình luận sôi nổi với hàng triệu người dùng

### 1.2. Tổng Quan Dự Án
Dự án này là một hệ thống crawler tự động thu thập dữ liệu từ trang tin tức VnExpress (https://vnexpress.net). Hệ thống được xây dựng bằng Python với khả năng thu thập đa luồng, xử lý lỗi thông minh và hỗ trợ nhiều định dạng lưu trữ dữ liệu. Dữ liệu thu thập được có thể sử dụng cho nhiều mục đích như:

- Phân tích xu hướng tin tức
- Nghiên cứu dư luận xã hội
- Xây dựng bộ dữ liệu cho AI/ML
- Theo dõi thông tin thị trường

## 2. Công Nghệ Sử Dụng

### 2.1. Ngôn Ngữ và Framework
- **Python 3.x**: Ngôn ngữ lập trình chính
- **aiohttp**: Thư viện HTTP bất đồng bộ cho việc crawl dữ liệu
- **BeautifulSoup4**: Thư viện phân tích HTML
- **SQLite**: Cơ sở dữ liệu nhẹ để lưu trữ dữ liệu

### 2.2. Thư Viện Chính
```
requests>=2.31.0
beautifulsoup4>=4.12.2
pandas>=2.1.0
aiohttp>=3.9.1
asyncio>=3.4.3
python-dotenv>=1.0.0
tqdm>=4.66.1
lxml>=4.9.3
```

### 2.3. Công Cụ Hỗ Trợ
- **Docker**: Đóng gói và triển khai
- **Logging**: Ghi log hệ thống
- **Progress Bar**: Hiển thị tiến trình crawl

## 3. Cấu Trúc Dự Án

### 3.1. Tệp Tin Chính
- `crawler.py`: File chính điều khiển quá trình crawl
- `fetcher.py`: Module tải dữ liệu từ web
- `parser.py`: Module phân tích HTML
- `saver.py`: Module lưu trữ dữ liệu
- `config.py`: Cấu hình hệ thống
- `.env`: File cấu hình môi trường

### 3.2. Thư Mục Output
- `output/articles.json`: Dữ liệu dạng JSON
- `output/articles.csv`: Dữ liệu dạng CSV
- `output/articles.db`: Cơ sở dữ liệu SQLite
- `output/crawler.log`: File log hệ thống

## 4. Tính Năng Chính

### 4.1. Thu Thập Dữ Liệu
- Thu thập đa luồng với aiohttp
- Hỗ trợ nhiều chuyên mục (thời sự, thế giới, kinh doanh, giải trí)
- Tự động retry khi gặp lỗi
- Progress bar hiển thị tiến trình

### 4.2. Xử Lý Dữ Liệu
- Phân tích HTML thông minh với BeautifulSoup4
- Làm sạch và chuẩn hóa dữ liệu
- Trích xuất metadata đầy đủ

### 4.3. Lưu Trữ Dữ Liệu
- Hỗ trợ nhiều định dạng (JSON, CSV, SQLite)
- Tự động tạo schema database
- Xử lý trùng lặp thông minh

## 5. Hướng Dẫn Sử Dụng

### 5.1. Cài Đặt
```bash
# Clone dự án
git clone https://github.com/PhamNhatKhanhs/datas.git

# Cài đặt dependencies
pip install -r requirements.txt
```

### 5.2. Cấu Hình
Chỉnh sửa file `.env`:
```env
BASE_URL=https://vnexpress.net
OUTPUT_FORMAT=json
CONCURRENT_REQUESTS=5
MAX_RETRIES=3
```

### 5.3. Chạy Crawler
```bash
python crawler.py
```

## 6. Đóng Góp
Mọi đóng góp và góp ý đều được hoan nghênh. Vui lòng tạo issue hoặc pull request tại [GitHub repository](https://github.com/PhamNhatKhanhs/datas).

## 7. Giấy Phép
Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
