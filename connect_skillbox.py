import os
from time import sleep
from dotenv import load_dotenv
import gzip

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from parse_m3u8 import get_chunk_m3u8, parse_m3u8


load_dotenv()


def authentication(driver):
    driver.find_element(By.CLASS_NAME, "cookie__button").click()

    login_input = driver.find_element(By.ID, "ui-sb-input-element-0")
    login_input.clear()
    login_input.send_keys(os.getenv('SKILLBOX_LOGIN'))

    pass_input = driver.find_element(By.ID, "ui-sb-input-element-1")
    pass_input.clear()
    pass_input.send_keys(os.getenv('SKILLBOX_PASS'))

    sleep(2)

    login_button = driver.find_element(By.TAG_NAME, "button").click()

    sleep(10)


def save_page(url, driver, path):
    driver.get(url)
    sleep(10)

    # Save page to html
    filename = path + 'index.html'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
        print(f'Страница сохранена в файл {filename}')

    # Take screenshot
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    print('Высота страницы:', height)
    height = 6000
    driver.set_window_size(1920, height)
    element = driver.find_element(By.TAG_NAME, 'body')
    element.screenshot(path + "screenshot.png")
    print(
        f'Скриншот сохранен в файл {path}screenshot.png')


def connection(url):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--incognito')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    s = Service(executable_path='./drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)

    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.maximize_window()
    driver.get(url)

    return driver


def save_video(driver, lesson_path, url) -> None:
    video_path = lesson_path + "videolesson.mp4"
    print('--------------Зашли в save_video------------------')

    try:
        is_video = driver.find_element(By.TAG_NAME, "video")
    except Exception:
        is_video = None

    if os.path.exists(video_path):
        print(f'Видео {video_path} уже существует')
        is_video = None

    print('is_video = ', is_video)
    if is_video:
        # driver.get(url)
        # sleep(10)

        for req in driver.requests:
            if 'playlist.m3u8' in req.url:
                chunklist = get_chunk_m3u8(req)
            if 'https://play.skillbox.ru/api/process/' in req.url:
                key = req.response.body
                key = gzip.decompress(key).decode('utf-8').encode('utf-8')
                print(f'Ключик: {key}')

        if chunklist and key:
            res = parse_m3u8(chunklist, key, video_path)
            print(f'\nПуть к видео урока: {res}')


def save_additional_materials():
    pass


if __name__ == '__main__':
    url = 'https://go.skillbox.ru/auth/sign-in'
    # url = 'https://habr.com/ru/companies/otus/articles/596071/'
    url2 = 'https://go.skillbox.ru/profession/professional-retraining-python-developer/dpo-django-framework/f006f924-a90e-4b84-839f-2d6f0f1f26bf/videolesson'

    try:
        driver = connection(url)
        sleep(5)

        '''аунтетификация'''
        authentication(driver)
        sleep(4)

        '''get playlist'''
        driver.get(url2)
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
        # driver.get(url2)
        # sleep(5)

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
        print('Done! '*10)
    pass
