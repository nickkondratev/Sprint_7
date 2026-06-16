import requests
import allure
from data import BASE_URL
from helpers import generate_random_string

class TestLoginCourier:

    @allure.step("Отправка запроса на авторизацию")
    def login_request(self, payload):
        return requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = self.login_request(payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Авторизация без логина')
    def test_login_without_login(self, courier):
        payload = {
            "password": courier["password"]
        }
        response = self.login_request(payload)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title('Авторизация с неверным паролем')
    def test_login_wrong_password(self, courier):
        payload = {
            "login": courier["login"],
            "password": "wrong_password"
        }
        response = self.login_request(payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title('Авторизация несуществующего курьера')
    def test_login_nonexistent_courier(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = self.login_request(payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]