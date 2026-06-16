import pytest
import requests
import allure
from data import BASE_URL
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def courier():
    """Создаёт курьера перед тестом и удаляет после"""
    login, password, first_name = register_new_courier_and_return_login_password()
    yield {"login": login, "password": password, "firstName": first_name}
    
    # Удаление курьера после теста
    login_data = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=login_data)
    if response.status_code == 200:
        courier_id = response.json()["id"]
        requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')