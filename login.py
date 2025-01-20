from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from utils import append_to_json_list


def login(name, password):
    user_data_dir = "chromeDb"
    profile_dir = name[:-11]
    print(profile_dir)
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile_dir}")
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('perfLoggingPrefs', {
        'enableNetwork': True,
        'enablePage': False,
    })

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        wait = WebDriverWait(driver, 20)

        driver.get("https://www.coursera.org/learn/research-methods?authMode=login")
        # time.sleep(5)
        # Wait for the email input field to appear
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(name)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        if "research-methods" in driver.current_url:
            print("Đăng nhập thành công!")
        else:
            print("Đăng nhập thất bại!")
        append_to_json_list('list_account.json', profile_dir)
        time.sleep(150)
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")


