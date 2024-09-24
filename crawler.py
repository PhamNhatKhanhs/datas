from fetcher import fetch_home_page
from parser import parse_titles
from saver import save_to_csv, save_to_json
import config

def main():
    # Lấy dữ liệu từ trang chủ
    pages = fetch_home_page(config.BASE_URL)
    
    # Phân tích tiêu đề từ trang
    all_titles = []
    for page in pages:
        titles = parse_titles(page)
        all_titles.extend(titles)

    # Lưu trữ dữ liệu
    if config.OUTPUT_FORMAT == "csv":
        save_to_csv(all_titles)
    elif config.OUTPUT_FORMAT == "json":
        save_to_json(all_titles)
    
    print(f"Hoàn thành! Dữ liệu đã được lưu dưới dạng {config.OUTPUT_FORMAT}.")

if __name__ == "__main__":
    main()
