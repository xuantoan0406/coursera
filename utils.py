import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import json
import os


def append_to_json_list(file_path, new_item):

    if os.path.exists(file_path):
        # Đọc dữ liệu hiện tại từ file JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    if not isinstance(data, list):
        raise ValueError("Dữ liệu trong file JSON không phải là danh sách!")

    # Thêm phần tử mới vào danh sách
    if new_item not in data:  # Kiểm tra để tránh trùng lặp
        data.append(new_item)

    # Ghi dữ liệu mới vào file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Sử dụng hàm
# file_path = "data.json"
# append_to_json_list(file_path, "hu4")


def read_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


def skip_video_forward(driver,num_skips):
    try:
        # Chờ cho nút "tua nhanh 10 giây" xuất hiện
        skip_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Seek Video Forward 10 seconds"]'))
        )

        # Tự động click vào nút tua nhanh nhiều lần
        for _ in range(num_skips):
            skip_button.click()
            time.sleep(0.5)  # Chờ 0.5 giây giữa mỗi lần click
    except Exception as e:
        print("Lỗi khi tìm nút tua nhanh:", e)
    # skip_button = driver.find_element(By.XPATH, '//button[@aria-label="Seek Video Forward 10 seconds"]')
    #
    # # Số lần tua nhanh
    # # num_skips = 10
    #
    # # Tự động click vào nút tua nhanh nhiều lần
    # for _ in range(num_skips):
    #     skip_button.click()
    #     time.sleep(0.5)
import re

def extract_number(text):
    # Use regular expression to find the first sequence of digits
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())  # Convert the matched string to an integer
    return None