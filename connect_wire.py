from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from time import sleep
import os


def wire_connection(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    # options.add_argument('--incognito')
    
    #path = 'C:\\Users\\heist\\PycharmProjects\\parsing_skillbox\\sources\\Итоговая аттестация по программе профессиональной \\1.Итоговая аттестация по программе профессиональной \\1.Описание итоговой аттестации\\'
    #options.add_experimental_option("prefs", {"download.default_directory": f'{path}'})

    options.add_argument(f'user-data-dir={os.getcwd()}/selenium')
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("—disable-blink-features=AutomationControlled")

    s = Service(executable_path='./drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

    # stealth(driver,
    #        languages=["ru-RU", "ru"],
    #        vendor="Google Inc.",
    #        platform="Win32",
    #        webgl_vendor="Intel Inc.",
    #        renderer="Intel Iris OpenGL Engine",
    #        fix_hairline=True,
    #        )

    driver.get(url)
    sleep(10)

    return driver


if __name__ == '__main__':
    # url = 'https://go.skillbox.ru/profession/professional-retraining-python-developer'
    # url2 = 'https://go.skillbox.ru/profession/professional-retraining-python-developer/dpo-django-framework/f006f924-a90e-4b84-839f-2d6f0f1f26bf/videolesson'
    url = 'https://fruitlab.com/video/aTUqTrJrMtj6FgO5?ntp=ggm'

    # authentication(driver)
    # driver.get(url)
    # sleep(10)

    # print(driver.requests)
    # for req in driver.requests:
    #    if 'ru.json' in req.url:
    #        print(req.url)
    #        print(req.ws_messages)

    driver = wire_connection(url)

    # driver.find_element(By.CLASS_NAME, "cookie__button").click()

    # authentication(driver)

    '''get playlist'''
    # driver.get(url2)
    # sleep(10)

    # input()
    for req in driver.requests:
        if 'aTUqTrJrMtj6FgO5.m3u8' in req.url:
            # r = requests.get(req.url)
            lines = req.response.body.decode('utf-8')
            print(lines)
            for line in lines.split():
                print(line)

            driver.close()
            driver.quit()
