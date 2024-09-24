# Sử dụng Python image
FROM python:3.9-slim

# Tạo thư mục làm việc
WORKDIR /app

# Copy file cần thiết
COPY . .

# Cài đặt thư viện
RUN pip install -r requirements.txt

# Chạy chương trình
CMD ["python", "crawler.py"]
