import os
import pickle
from time import sleep
from dotenv import load_dotenv
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_stealth import stealth


load_dotenv()


def authentication(driver):
    login_input = driver.find_element(By.ID, "ui-sb-input-element-0")
    login_input.clear()
    login_input.send_keys(os.getenv('SKILLBOX_LOGIN'))

    pass_input = driver.find_element(By.ID, "ui-sb-input-element-1")
    pass_input.clear()
    pass_input.send_keys(os.getenv('SKILLBOX_PASS'))

    sleep(2)

    login_button = driver.find_element(By.TAG_NAME, "button").click()

    sleep(2)


def save_page(url, driver):
    driver.get(url)
    sleep(5)

    with open('lesson.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)


if __name__ == '__main__':
    url = 'https://go.skillbox.ru/profession/professional-retraining-python-developer'
    url2 = 'https://go.skillbox.ru/profession/professional-retraining-python-developer/dpo-python-basic/2e40f153-c827-42e3-a7f0-c25528b1af8e/videolesson'
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    s = Service(
        executable_path='C:\\Users\\heist\\PycharmProjects\\parsing_skillbox\\chromedriver_win32\\chromedriver.exe')

    driver = webdriver.Chrome(service=s, options=options)

    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    try:
        driver.maximize_window()
        driver.get(url)
        sleep(2)

        '''аунтетификация'''
        authentication(driver)
        sleep(4)

        '''dump cookies'''
        # pickle.dump(driver.get_cookies(), open('cookies', 'wb'))

        '''add cookies'''
        # for cookie in pickle.load(open('cookies', 'rb')):
        #    driver.add_cookie(cookie)
        # sleep(2)
        # driver.refresh()
        # sleep(2)

        # goto video
        driver.get(url2)

        link = input('Введите blob адрес видео: ')

        r = requests.get(link)
        print(r.content)
        with open('video.html', 'wb', encoding='utf-8') as f:
            f.write(r.content)

        # save_page(url2, driver)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
