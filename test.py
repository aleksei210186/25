#  Запуск   -   python -m pytest -v --driver Chrome --driver-path chromedriver.exe test.py


import pytest
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver')
    # устанавливаем неявное ожидание
    pytest.driver.implicitly_wait(10)
    # Увеличиваем размер окна браузера на весь экран
    pytest.driver.maximize_window()

    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('aaa@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('123456')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на ссылку "Мои питомцы"
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    # Сохраняем скриншот страницы "Мои питомцы"
    pytest.driver.save_screenshot('my_pets.png')

    yield

    pytest.driver.quit()

# возвращаем число питомцев из блока статистики пользователя
@pytest.fixture()
def get_pets_num():
    acc_info = pytest.driver.find_elements(By.CSS_SELECTOR, 'div.task3 > div.left')[0].text
    #  Извлекаем из найденного текста информацию про количество питомцев
    pets_num = acc_info.split()[4]

    # Проверяем, что число питомцев положительное или равно 0
    assert int(pets_num) >= 0

    return int(pets_num)

# получить значения имен, возрастов, пород из таблицы с питомцами
@pytest.fixture()
def get_pets_info():
    #names, ages, types = [], [], []
    # находим все имена питомцев
    names = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(1)')
    # находим все возраста питомцев
    ages = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(2)')
    # находим все породы питомцев
    types = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody > tr > td:nth-of-type(3)')

    # преобразуем найденные элементы в текстовый список имен
    text_names = [names[i].text for i in range(len(names))]
    # преобразуем найденные элементы в текстовый список возрастов
    text_ages = [ages[i].text for i in range(len(ages))]
    # преобразуем найденные элементы в текстовый список пород
    text_types = [types[i].text for i in range(len(types))]

    return text_names, text_ages, text_types


# проверяем, что присутствуют все питомцы
def test_all_my_pets_are_in_table(get_pets_num):
    table_rows = []
    try:
        table_rows = WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#all_my_pets > table tr'))
        )
    except TimeoutException:
        print("Не удалось загрузить элементы на странице")

    finally:
        assert get_pets_num == len(table_rows) - 1


# проверяем, что хотя бы у половины питомцев есть фото
def test_half_of_pets_have_photo(get_pets_num):
    photos = []
    try:
        photos = WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#all_my_pets > table img'))
        )
    except TimeoutException:
        print("Не удалось загрузить элементы на странице")

    finally:
        photo_count = 0
        for i in range(len(photos)):
            if photos[i].get_attribute('src') != '':
                photo_count += 1
        assert photo_count >= get_pets_num / 2


# проверяем, что у всех питомцев есть имя, возраст и порода
def test_pets_have_name_age_type(get_pets_info):
    names, ages, types = get_pets_info
    for i in range(len(names)):
        assert names[i] != ''
        assert ages[i] != ''
        assert types[i] != ''

# проверяем, что у всех питомцев разные имена
def test_pets_have_diff_name(get_pets_num, get_pets_info):
    names, ages, types = get_pets_info
    pets = {}
    for i in range(len(names)):
        pets[names[i]] = (ages[i], types[i])

    assert get_pets_num == len(pets)

# проверяем, что в списке нет повторяющихся питомцев
def test_all_pets_are_unique(get_pets_info):
    names, ages, types = get_pets_info
    flag = True

    for i in range(len(names) - 1):
        for j in range(i + 1, len(names)):
            if names[i] == names[j] and ages[i] == ages[j] and types[i] == types[j]:
                flag = False
                break
        if not flag:
            break

    assert flag == True