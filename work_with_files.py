import json
import os
import regex
from connect_skillbox import save_page, save_video, save_additional_materials, take_screenshot
from time import sleep


def json_to_dict(dictjson: str) -> dict:
    """
    Получает ссылку на json файл, переводит его в словарь
    и возвращает

    Args:
        dictjson (dict): _description_

    Returns:
        dict: _description_
    """
    with open(dictjson, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def add_dir(rpath: str, dirname: str, num=None) -> str:
    """
    Проверяет, существует ли дирректория, если нет, 
    то содает и возвращает в виде строки

    Args:
        rpath (_type_): _description_
        dirname (_type_): _description_
        num (_type_, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    if num:
        path = rpath + f'{str(num)}.{dirname}' + '/'
    else:
        path = rpath + dirname + '/'

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            return add_dir(rpath, 'ERROR_переназови', num)
        print(f'Создана папка: {path}')

    return path


def clear_module_name(module_name: str) -> str:
    """
    Чистит имя модуля от лишних символов и возвращает строку

    Args:
        module_name (_type_): _description_

    Returns:
        str: _description_
    """
    try:
        module_name = regex.sub(r'[^\pL\p{Space}-]', '', module_name[:50])
    except:
        module_name = 'ERROR_переназови'
    print('Очищеное имя модуля: ' + f'{module_name}'.upper())

    return module_name


def make_url(base_url: str, url_name: str) -> str:
    """
    Возвращает строку с адресом модуля

    Args:
        base_url (str): _description_
        url_name (str): _description_

    Returns:
        str: _description_
    """
    res = base_url + url_name + '/'
    print(f'Адрес модуля: {res}')
    return res


def get_lessons_list(topic: dict) -> list:
    """
    Возвращает список уроков

    Args:
        topics (_type_): _description_

    Returns:
        list: _description_
    """
    res = []

    key_list = ('homeworks', 'videolessons', 'tests', 'longreads')
    for key, val in topic.items():
        if key in key_list and len(val) > 0:
            for i in val:
                res.append(i)

    print(f'Количество уроков в модуле = {len(res)}')
    return res


def get_lessons(lessons_list, slug_url, module_path, driver) -> None:
    for lesson in lessons_list:
        id = lesson.get('id')
        number = lesson.get('number')
        name = lesson.get('name')
        lesson_type = lesson.get('lesson_type')

        if id and number and name and lesson_type:
            # Создаем папку урока
            lesson_name = clear_module_name(name)
            lesson_path = add_dir(module_path, lesson_name, number)

            # Создаем ссылку на урок
            url_name = f'{id}/{lesson_type}'
            lesson_url = make_url(slug_url, url_name)

            # Переходим на страницу, ждем 10 сек.
            while True:
                try:
                    print(f'driver.get({lesson_url})')
                    driver.get(lesson_url)
                    sleep(10)
                    break
                except Exception as ex:
                    print('!'*100, ex, sep='\n')

            # Сохраняем страницу
            # save_page(driver, lesson_path)

            # Делаем скриншот
            # take_screenshot(driver, lesson_path)

            # Качаем видео, если оно есть на странице
            # save_video(driver, lesson_path, lesson_url)

            # Сохраняем доп.материалы, если они есть
            save_additional_materials(driver, lesson_path, lesson_url)
