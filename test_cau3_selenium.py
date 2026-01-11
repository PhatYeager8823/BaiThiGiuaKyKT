import time
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH WEB (OPENCART) ---
CONFIG = {
    "URL": "http://opencart.abstracta.us/",
    "SEARCH_BOX_NAME": "search",
    "KEYWORD": "Mac",
    "RESULT_ITEM_CLASS": "product-thumb",
    "TITLE_TAG": "h4",
    "LINK_TAG": "a"
}

# --- HÀM LƯU VÀO DB MỚI ---
def save_to_sql_server(data):
    print("-> Đang kết nối SQL Server...")
    try:
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=YOUR_SERVER_NAME;'  # <--- NHỚ SỬA TÊN MÁY BẠN
            'Database=QuanLyKetQuaCrawl;' # <--- DB MỚI CỦA BẠN
            'Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        # Code tự tạo bảng nếu chưa có
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='KetQuaTimKiem' and xtype='U')
            CREATE TABLE KetQuaTimKiem (
                STT INT PRIMARY KEY IDENTITY(1,1),
                TenBai NVARCHAR(MAX),
                Link NVARCHAR(MAX)
            )
        """)
        
        # Xóa dữ liệu cũ trong bảng này (nếu chạy lại nhiều lần)
        cursor.execute("TRUNCATE TABLE KetQuaTimKiem")

        for row in data:
            cursor.execute("INSERT INTO KetQuaTimKiem (TenBai, Link) VALUES (?, ?)", 
                           row['title'], row['link'])
        
        conn.commit()
        conn.close()
        print(f"-> Đã lưu thành công {len(data)} sản phẩm vào DB 'QuanLyKetQuaCrawl'!")
        
    except Exception as e:
        print("❌ LỖI SQL:", e)
        print("👉 Gợi ý: Bạn đã chạy lệnh 'CREATE DATABASE QuanLyKetQuaCrawl' trong SQL Server chưa?")

# --- LOGIC SELENIUM (GIỮ NGUYÊN) ---
def test_cau3_opencart():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    results = []

    try:
        driver.get(CONFIG['URL'])
        driver.maximize_window()
        time.sleep(2)

        try:
            search_box = driver.find_element(By.NAME, CONFIG['SEARCH_BOX_NAME'])
            search_box.clear()
            search_box.send_keys(CONFIG['KEYWORD'])
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return

        items = driver.find_elements(By.CLASS_NAME, CONFIG['RESULT_ITEM_CLASS'])
        print(f"✅ Tìm thấy {len(items)} sản phẩm.")

        for item in items:
            try:
                title_elem = item.find_element(By.TAG_NAME, CONFIG['TITLE_TAG'])
                title = title_elem.text
                link = title_elem.find_element(By.TAG_NAME, CONFIG['LINK_TAG']).get_attribute("href")
                
                print(f"   - {title}")
                results.append({"title": title, "link": link})
            except:
                continue

    except Exception as e:
        print("Lỗi Selenium:", e)
    finally:
        driver.quit()

    if results:
        save_to_sql_server(results)

if __name__ == "__main__":
    test_cau3_opencart()