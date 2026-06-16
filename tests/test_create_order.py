import requests
import pytest
import allure
from data import BASE_URL

class TestCreateOrder:

    @allure.step("Отправка запроса на создание заказа")
    def create_order_request(self, payload):
        return requests.post(f'{BASE_URL}/api/v1/orders', json=payload)

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title('Создание заказа с цветом: {color}')
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        response = self.create_order_request(payload)
        assert response.status_code == 201
        assert "track" in response.json()