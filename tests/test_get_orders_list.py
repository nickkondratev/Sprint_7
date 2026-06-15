import requests
import allure
from data import BASE_URL

class TestGetOrdersList:

    @allure.title('Получение списка заказов')
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)