from selenium import webdriver
from selenium.webdriver.common.by import By
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
from utils import skip_video_forward, extract_number

user_data_dir = "chromeDb"
chrome_options = Options()


def auto_watch_video(account, link_video):
    profile_dir = account
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
        driver.get(link_video)
        # driver.get("https://www.coursera.org/learn/research-methods/home/week/2")

        items = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//a[contains(@data-click-key, "open_course_home.period_page.click.item_link")]')
        ))

        for i, item in enumerate(items):
            type_element = item.find_element(By.XPATH,
                                             './/div[contains(text(), "Video") or contains(text(), "Reading")]')
            item_type = type_element.text
            title = item.find_element(By.XPATH, './/p[@data-test="rc-ItemName"]').text

            try:
                duration = item.find_element(By.XPATH, './/span[contains(text(), "min")]').text
                print(f"duration:{duration},{title}")
            except:
                duration = item.find_element(By.XPATH, './/span[contains(text(), "sec")]').text
                print(f"duration:{duration},{title}")
            print(f"title : {title} - time: {duration}")

            if "Reading" in item_type:
                print("readdddddddddd")
                item.click()
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    next_item_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-item']")))
                    next_item_button.click()
                    print("Clicked 'Go to next item' button.")
                    for i in range(14):
                        skip_video_forward(driver, 20)
                    # time.sleep(100)
                    # run_video(driver, duration)
                except Exception as e:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("Could not find or click 'Go to next item' button:", e)
                    time.sleep(35)
                    button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='mark-complete']")))
                    button.click()
                    time.sleep(2)
                    next_item_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-item']")))
                    next_item_button.click()
                    print("Clicked 'Go to next item' button.")
                    print("da click")
                    time.sleep(2)
                    # num_skip = int(duration[0]) * 6
                    for i in range(14):
                        skip_video_forward(driver, 20)
                    # time.sleep(120)

            elif "Video" in item_type:
                item.click()
                print(duration)
                # run_video(driver, duration)
                time.sleep(3)
                try:
                    num_skip = int(duration[0]) * 6
                    for i in range(14):
                        skip_video_forward(driver, 20)
                    # time.sleep(120)
                except:
                    continue
            # driver.back()
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

    finally:
        # Close the browser
        driver.quit()


for i in range(1, 5):
    print(i)
    auto_watch_video("quynhptnss181190", f"https://www.coursera.org/learn/research-methods/home/week/{i}")
