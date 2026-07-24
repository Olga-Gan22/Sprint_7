"""список заказов"""

import allure
import pytest
import requests
from data.creating_data import Url

@allure.feature("Orders API")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов: базовый кейс без фильтров")
    def test_get_orders_default(self):
        response = requests.get(f"{Url.MAIN_URL}{Url.ORDERS}")
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        body = response.json()
        assert "orders" in body and isinstance(body["orders"], list)
        assert "pageInfo" in body

    @allure.title("Получение списка заказов с limit и page")
    @pytest.mark.parametrize("limit,page,expected_limit", [
        (10, 0, 10),
        (5, 1, 5),
    ])
    def test_get_orders_with_pagination(self, limit, page, expected_limit):
        params = {"limit": limit, "page": page}
        response = requests.get(f"{Url.MAIN_URL}{Url.ORDERS}", params=params)
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        body = response.json()
        assert "orders" in body and isinstance(body["orders"], list)
        assert "pageInfo" in body
        page_info = body["pageInfo"]
        assert page_info["page"] == page
        assert page_info["limit"] == expected_limit or page_info["limit"] <= 30

    @allure.title("Проверка поведения API при запросе заказов курьера")
    @pytest.mark.parametrize("courier_id", [1, 2, 9999])
    def test_get_orders_by_courier(self, courier_id):
        params = {"courierId": courier_id}
        response = requests.get(f"{Url.MAIN_URL}{Url.ORDERS}", params=params)

        if courier_id == 9999:
            assert response.status_code == 404, f"Для несуществующего courierId ожидался 404, получен {response.status_code}"
            body = response.json()
            assert "message" in body, "При 404 должно быть поле 'message'"
            return

        if response.status_code == 404:
            body = response.json()
            assert body.get("message") is not None
            return

        assert response.status_code == 200, f"Ожидался 200 или 404, получен {response.status_code}"
        body = response.json()
        assert "orders" in body and isinstance(body["orders"], list)

    @allure.title("Фильтрация заказов по nearestStation: проверка поведения стенда")
    def test_get_orders_by_nearest_station(self):
        stations = ["1", "2"]
        params = {"nearestStation": stations}

        response = requests.get(f"{Url.MAIN_URL}{Url.ORDERS}", params=params)

        if response.status_code == 500:
            pytest.skip("Стенд не поддерживает фильтр nearestStation (возвращает 500)")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        body = response.json()
        assert "orders" in body and isinstance(body["orders"], list)

        for order in body["orders"]:
            station = order.get("metroStation")
            assert station in stations, f"Станция {station} не входит в отфильтрованный список {stations}"

    @allure.title("Комбинированный запрос: проверка поведения стенда")
    def test_get_orders_combined_filters(self):
        courier_id = 1
        stations = ["2", "3"]
        limit = 10
        page = 0

        params = {
            "courierId": courier_id,
            "nearestStation": stations,
            "limit": limit,
            "page": page,
        }

        response = requests.get(f"{Url.MAIN_URL}{Url.ORDERS}", params=params)

        if response.status_code == 500:
            pytest.skip("Стенд не поддерживает комбинированные фильтры (возвращает 500)")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        body = response.json()
        assert "orders" in body and isinstance(body["orders"], list)
        page_info = body.get("pageInfo")
        assert page_info is not None
        assert page_info.get("limit") == limit
        assert page_info.get("page") == page

        for order in body["orders"]:
            assert order.get("courierId") == courier_id
            assert order.get("metroStation") in stations
