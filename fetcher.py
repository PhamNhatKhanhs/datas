import requests

def fetch_page(url):
    """Gửi yêu cầu HTTP đến URL và trả về nội dung HTML."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối đến {url}: {e}")
        return None

# Không cần fetch nhiều trang do VnExpress không có URL dạng /page/1, /page/2
def fetch_home_page(base_url):
    """Lấy dữ liệu từ trang chủ của VnExpress."""
    print(f"Đang lấy dữ liệu từ: {base_url}")
    html = fetch_page(base_url)
    return [html] if html else []
