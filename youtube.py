import os
import json
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


def save_cookie(driver, path):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)


def load_cookie(driver, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        driver.add_cookie(cookie)


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

    filename = url.split('/')[-1] + '.html'

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)


if __name__ == '__main__':
    url = 'https://my.infobox.ru/#/login/'
    url2 = 'https://www.youtube.com/watch?v=sHPggeUBO_o'
    options = webdriver.ChromeOptions()
    # options.add_argument('--incognito')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
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

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.3.821325282.1685912298; _ym_uid=1674484193502465472; _ym_d=1685912298; _ga=GA1.1.821325282.1685912298; _gid=GA1.3.390374194.1687127329; _ga_QYYHYDRQM6=GS1.1.1687127329.5.0.1687127329.0.0.0; _ym_isad=1; _ym_visorc=w',
        'If-Modified-Since': 'Fri, 16 Jun 2023 10:37:50 GMT',
        'If-None-Match': '"648c3b7e-71da"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        driver.maximize_window()
        driver.get(url)
        load_cookie(driver, 'infobox_cookies.json')
        sleep(5)

        '''аунтетификация'''
        # authentication(driver)
        # sleep(4)

        '''dump cookies'''
        # pickle.dump(driver.get_cookies(), open('cookies', 'wb'))
        # save_cookie(driver, 'infobox_cookies.json')

        '''add cookies'''
        # for cookie in pickle.load(open('cookies', 'rb')):
        #    driver.add_cookie(cookie)
        # sleep(5)
        # driver.add_cookie(cookies)
        load_cookie(driver, 'infobox_cookies.json')
        driver.refresh()
        sleep(5)

        # goto video
        # driver.get(url2)

        # link = input('Введите blob адрес видео: ')
        # r = requests.get(link)
        # print(r.content)
        # with open('video.html', 'wb', encoding='utf-8') as f:
        #    f.write(r.content)

        # save_page(url2, driver)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
