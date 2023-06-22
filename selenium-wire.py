from requests import get
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from selenium_stealth import stealth
from time import sleep


options = Options()
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("—disable-blink-features=AutomationControlled")

s = Service(executable_path='./drivers/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#    'source': '''
#            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
#            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
#            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
#      '''
# })

stealth(driver,
        languages=["ru-RU", "ru"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


if __name__ == '__main__':
    url = 'https://go.skillbox.ru/profession/professional-retraining-python-developer'

    driver.get(url)
    sleep(2)
    # input()

    for req in driver.requests:
        if 'ru.json' in req.url:
            print(req.url)
            print(req.ws_messages)

    driver.close()
    driver.quit()
