from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


def configure_driver(profile_dir, user_data_dir):
    """Cấu hình và khởi tạo WebDriver với profile riêng biệt"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile_dir}")
    # chrome_options.add_argument("--headless")  # Chạy không giao diện
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def click_element(driver, by, value, wait_time=10):
    """Tìm và click vào một element"""
    try:
        element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((by, value)))
        element.click()
        return element
    except Exception as e:
        print(f"Không thể click vào element ({value}): {e}")
        return None


def skip_video(driver):
    """Thực hiện thao tác bỏ qua video"""
    try:
        print("Skipping video...")
        driver.execute_script("document.querySelector('video').currentTime = document.querySelector('video').duration;")
    except Exception as e:
        print(f"Lỗi khi bỏ qua video: {e}")


def handle_item(driver, item, wait):
    """Xử lý từng mục học (Video hoặc Reading)"""
    try:
        type_element = item.find_element(By.XPATH, './/div[contains(text(), "Video") or contains(text(), "Reading")]')
        item_type = type_element.text
        title = item.find_element(By.XPATH, './/p[@data-test="rc-ItemName"]').text

        try:
            duration = item.find_element(By.XPATH, './/span[contains(text(), "min")]').text
        except:
            duration = item.find_element(By.XPATH, './/span[contains(text(), "sec")]').text

        print(f"Xử lý mục: {title} - Loại: {item_type} - Thời lượng: {duration}")

        # Xử lý mục Reading
        if "Reading" in item_type:
            item.click()
            time.sleep(2)
            scroll_and_click_next(driver, wait)

        # Xử lý mục Video
        elif "Video" in item_type:
            item.click()
            time.sleep(3)
            skip_video(driver)

    except Exception as e:
        print(f"Lỗi khi xử lý mục: {e}")


def scroll_and_click_next(driver, wait):
    """Cuộn xuống cuối trang và click nút 'Next'"""
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_item_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-item']")))
        next_item_button.click()
        print("Clicked 'Next Item' button.")
    except Exception as e:
        print(f"Lỗi khi cuộn trang và click Next: {e}")


def auto_watch_video(account, link_video, user_data_dir):
    """Tự động xem video và xử lý nội dung khóa học"""
    print(f"Đang chạy tài khoản: {account}")
    driver = configure_driver(account, user_data_dir)

    try:
        wait = WebDriverWait(driver, 20)

        # Truy cập liên kết video
        driver.get(link_video)
        time.sleep(5)

        # Click nút 'Enroll' nếu có
        click_element(driver, By.CSS_SELECTOR, '[data-e2e="enroll-button"]')

        # Click nút 'Go To Course'
        click_element(driver, By.CSS_SELECTOR, "button[data-e2e='fCKQimXqEeSuUyIAC0mIhA~courseHomeLink']")

        # Xử lý các mục học
        items = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//a[contains(@data-click-key, "open_course_home.period_page.click.item_link")]')
        ))

        for item in items:
            handle_item(driver, item, wait)

    except Exception as e:
        print(f"Lỗi trong quá trình chạy: {e}")

    finally:
        driver.quit()


# Gọi hàm với tài khoản và video cụ thể
account = "Anhdlss181144"
user_data_dir = "chromeDb"
link_video = "https://www.coursera.org/learn/research-methods/home/week/1"
auto_watch_video(account, link_video, user_data_dir)
