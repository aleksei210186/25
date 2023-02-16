import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver')
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('aaa@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя

    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

try:
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        print('NAME: ', names[i].text)
        assert names[i].text != ''
        assert descriptions[i].text != ''
        print('Descriptions: ', descriptions[i].text)
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
except:
    print('Отсутствует какая-то информация о питомце')