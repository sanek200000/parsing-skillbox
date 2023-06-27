from connect_skillbox import authentication
from work_with_files import json_to_dict, clear_module_name, add_dir, make_url, get_lessons_list, get_lessons
from connect_wire import wire_connection

if __name__ == '__main__':
    base_url = 'https://go.skillbox.ru/profession/professional-retraining-python-developer/'
    module_json = './trees/Модуль Система контроля версий Git.json'
    source_path = r"./sources/"

    try:
        # Зайти на страницу авторизации
        driver = wire_connection(base_url)

        # Авторизоваться
        authentication(driver)
    except Exception as ex:
        print(ex)

    # Создать словарь из json модуля
    try:
        module_dict = json_to_dict(module_json)
    except Exception:
        raise Exception

    # Создать папку с названием модуля
    module_name_dir = clear_module_name(module_dict.get('name'))
    module_path = add_dir(source_path, module_name_dir)

    # Сформировать url модуля
    slug_name = module_dict.get('slug')
    if slug_name:
        slug_url = make_url(base_url, slug_name)
    else:
        raise 'Нет ключа "slug" в словаре module_dict'

    # Циклом пройдем по списку уроков
    try:
        topics = module_dict.get('topics')
    except Exception as ex:
        topics = None
        print(ex)

    if topics:
        count = 100
        for topic in topics:
            try:
                topic_name = topic.get('name')
                topic_num = topic.get('number')
            except Exception as ex:
                topic_name = 'Unknown topic' + str(count)
                topic_num = str(count)

            # Создаем папку с именем топика
            topic_path = add_dir(module_path, topic_name, topic_num)

            # Проверяем ключи 'homeworks', 'videolessons', 'tests', 'longreads'
            lessons_list = get_lessons_list(topic)

            # Прогходим по каждому уроку в списке
            if len(lessons_list) > 0:
                get_lessons(lessons_list, slug_url, topic_path, driver)
