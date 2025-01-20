import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from utils import skip_video_forward, read_json, extract_number

user_data_dir = "chromeDb"
chrome_options = Options()


def skip_video(driver):
    for i in range(10):
        skip_video_forward(driver, 20)


def auto_watch_video(account, link_video):
    print("accounts:  ", accounts)
    profile_dir = account
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile_dir}")
    # chrome_options.add_argument("--remote-debugging-port=9210")  # Dùng cổng 9222 cho instance đầu tiên

    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('perfLoggingPrefs', {
        'enableNetwork': True,
        'enablePage': False,
    })
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        wait = WebDriverWait(driver, 20)
        driver.get(link_video)
        try:
            time.sleep(5)
            enroll_button = driver.find_element(By.CSS_SELECTOR, '[data-e2e="enroll-button"]')
            # Scroll to the button if necessary
            actions = ActionChains(driver)
            actions.move_to_element(enroll_button).perform()
            # Click the button
            enroll_button.click()
            time.sleep(2)
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continue']]"))

            )
            continue_button.click()
            time.sleep(3)
            go_to_course_button = driver.find_element(By.CSS_SELECTOR,
                                                      "button.cds-124.cds-button-disableElevation.cds-button-primary.css-73yprj[data-e2e='fCKQimXqEeSuUyIAC0mIhA~courseHomeLink']")

            # Click the button
            go_to_course_button.click()
            print("Clicked the 'Go To Course' button successfully!")
            # driver.get("https://www.coursera.org/learn/research-methods/home/week/2")
            driver.get(link_video)
        except:
            pass
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
                    skip_video(driver)
                    # time.sleep(100)
                    # run_video(driver, duration)
                except Exception as e:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("Could not find or click 'Go to next item' button:", e)
                    time.sleep(30)
                    button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='mark-complete']")))
                    button.click()
                    time.sleep(2)
                    next_item_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-item']")))
                    next_item_button.click()
                    time.sleep(2)
                    skip_video(driver)


            elif "Video" in item_type:
                item.click()
                print(duration)
                # run_video(driver, duration)
                time.sleep(3)
                try:
                    skip_video(driver)
                except:
                    continue
            # driver.back()
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

    finally:
        # Close the browser
        driver.quit()


def run_1_account(account):
    link_video = "https://www.coursera.org/learn/research-methods/home/week/"
    threads = []
    for task_id in range(1, 5):  # Mỗi tài khoản chạy 4 luồng
        t = threading.Thread(target=auto_watch_video, args=(account, link_video + str(task_id)))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"All tasks for Account {account} are completed.")


# auto_watch_video("nhanmtss181195", "https://www.coursera.org/learn/research-methods/home/week/1")
# run_1_account("quynhptnss181190")
accounts = read_json("list_account.json")
# accounts = ["thudmss181396",
#             "phatncss181178",
#             "Anhdlss181144", ]
threads = []
week1 = "https://www.coursera.org/learn/research-methods/home/week/1"
week2 = "https://www.coursera.org/learn/research-methods/home/week/2"
week3 = "https://www.coursera.org/learn/research-methods/home/week/3"
week4 = "https://www.coursera.org/learn/research-methods/home/week/4"


for i, account_name in enumerate(accounts[1:]):

    for k in range(1,5):
        auto_watch_video(account_name, f"https://www.coursera.org/learn/research-methods/home/week/{k}")
        print(i,k, account_name)
        time.sleep(4)
    #     print(account_name)
#     t = threading.Thread(target=auto_watch_video, args=(account_name, week2))
#     threads.append(t)
#     t.start()
#
# for t in threads:
#     t.join()

# for i in range(1, 5):
#     print(i)
#     auto_watch_video("hoangnmss181025", f"https://www.coursera.org/learn/research-methods/home/week/{i}")
