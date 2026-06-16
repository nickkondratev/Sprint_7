import requests
import allure
from data import BASE_URL
from helpers import generate_random_string

class TestCreateCourier:

    @allure.step("Отправка запроса на создание курьера")
    def create_courier_request(self, payload):
        return requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = self.create_courier_request(payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        # Удаление созданного курьера
        login_data = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=login_data)
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"],
            "firstName": courier["firstName"]
        }
        response = self.create_courier_request(payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.title('Создание курьера без обязательного поля login')
    def test_create_courier_without_login(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = self.create_courier_request(payload)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title('Создание курьера без обязательного поля password')
    def test_create_courier_without_password(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = self.create_courier_request(payload)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]