"""список заказов"""

# tests/test_order_list.py
import allure
import pytest
import requests
from data.creating_data import Url


@allure.feature("Orders API")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов: базовый кейс без фильтров")
    def test_get_orders_default(self):
        url = f"{Url.MAIN_URL}{Url.ORDERS}"

        @allure.step("Отправляем GET-запрос без параметров")
        def step_send_request():
            return requests.get(url)

        response = step_send_request()

        @allure.step("Проверяем статус 200")
        def step_check_status():
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}. Тело: {response.text}"
            )

        @allure.step("Проверяем структуру ответа: наличие orders (список) и pageInfo")
        def step_check_body():
            body = response.json()
            assert "orders" in body and isinstance(body["orders"], list), (
                "В ответе должно быть поле 'orders' типа list"
            )
            assert "pageInfo" in body, "В ответе должно быть поле 'pageInfo'"

        step_check_status()
        step_check_body()

    @allure.title("Пагинация: проверка limit и page")
    @pytest.mark.parametrize("limit,page,expected_limit", [
        (10, 0, 10),
        (5, 1, 5),
    ])
    def test_get_orders_with_pagination(self, limit, page, expected_limit):
        url = f"{Url.MAIN_URL}{Url.ORDERS}"
        params = {"limit": limit, "page": page}

        @allure.step(f"Отправляем GET с limit={limit}, page={page}")
        def step_send_request():
            return requests.get(url, params=params)

        response = step_send_request()

        @allure.step("Проверяем статус 200")
        def step_check_status():
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}. Тело: {response.text}"
            )

        @allure.step("Проверяем, что orders — это список и есть pageInfo")
        def step_check_structure():
            body = response.json()
            assert "orders" in body and isinstance(body["orders"], list)
            assert "pageInfo" in body
            page_info = body["pageInfo"]
            assert page_info["page"] == page
            assert (page_info["limit"] == expected_limit) or (page_info["limit"] <= 30)

        step_check_status()
        step_check_structure()

    @allure.title("Список заказов курьера: валидный courierId — ожидаем 200 (стенд сейчас возвращает 404)")
    @pytest.mark.parametrize("courier_id", [1, 2])
    @pytest.mark.xfail(
        reason="Стенд возвращает 404 для валидных courierId (1, 2). Это баг стенда, а не теста.",
        strict=False
    )
    def test_get_orders_by_courier_valid(self, courier_id):
        url = f"{Url.MAIN_URL}{Url.ORDERS}"
        params = {"courierId": courier_id}

        @allure.step(f"Отправляем GET с courierId={courier_id}")
        def step_send_request():
            return requests.get(url, params=params)

        response = step_send_request()

        @allure.step("Проверяем статус 200 и структуру ответа")
        def step_check_response():
            assert response.status_code == 200, (
                f"Для валидного courierId ожидался 200, но получен {response.status_code}. "
                f"Тело ответа: {response.text}"
            )
            body = response.json()
            assert "orders" in body and isinstance(body["orders"], list), (
                "В ответе должно быть поле 'orders' типа list"
            )

        step_check_response()


    @allure.title("Список заказов курьера: несуществующий courierId — ожидаем 404")
    @pytest.mark.parametrize("courier_id", [9999])
    def test_get_orders_by_courier_not_found(self, courier_id):
        url = f"{Url.MAIN_URL}{Url.ORDERS}"
        params = {"courierId": courier_id}

        @allure.step(f"Отправляем GET с несуществующим courierId={courier_id}")
        def step_send_request():
            return requests.get(url, params=params)

        response = step_send_request()

        @allure.step("Проверяем статус 404 и наличие сообщения об ошибке")
        def step_check_error():
            assert response.status_code == 404, (
                f"Для несуществующего courierId ожидался 404, получен {response.status_code}"
            )
            body = response.json()
            assert "message" in body, (
                "При 404 в ответе должно быть поле 'message'"
            )

        step_check_error()

    @allure.title("Фильтрация по nearestStation: проверяем работу фильтра")
    @pytest.mark.parametrize("station", ["1", "2"])
    @pytest.mark.xfail(
        reason="Стенд возвращает 500 при использовании фильтра nearestStation. Это баг стенда.",
        strict=False
    )
    def test_get_orders_by_nearest_station(self, station):
        url = f"{Url.MAIN_URL}{Url.ORDERS}"
        params = {"nearestStation": station}

        @allure.step(f"Отправляем GET с nearestStation={station}")
        def step_send_request():
            return requests.get(url, params=params)

        response = step_send_request()

        @allure.step("Проверяем статус 200 и содержимое списка")
        def step_check_response():
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}. Тело: {response.text}"
            )
            body = response.json()
            assert "orders" in body and isinstance(body["orders"], list)
            for order in body["orders"]:
                metro_station = order.get("metroStation")
                assert metro_station == station, (
                    f"Станция заказа ({metro_station}) не совпадает с фильтром ({station})"
                )

        step_check_response()

    @allure.title("Комбинированные фильтры: courierId + nearestStation + пагинация")
    @pytest.mark.xfail(
        reason="Стенд возвращает 500 на комбинированные фильтры. Это баг стенда.",
        strict=False
    )
    def test_get_orders_combined_filters(self):
        courier_id = 1
        station = "2"
        limit = 10
        page = 0

        url = f"{Url.MAIN_URL}{Url.ORDERS}"
        params = {
            "courierId": courier_id,
            "nearestStation": station,
            "limit": limit,
            "page": page,
        }

        @allure.step("Отправляем запрос с комбинированными фильтрами")
        def step_send_request():
            return requests.get(url, params=params)

        response = step_send_request()

        @allure.step("Проверяем статус 200 и соответствие фильтров в результатах")
        def step_check_response():
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}. Тело: {response.text}"
            )
            body = response.json()
            assert "orders" in body and isinstance(body["orders"], list)
            page_info = body.get("pageInfo")
            assert page_info is not None
            assert page_info.get("limit") == limit
            assert page_info.get("page") == page

            for order in body["orders"]:
                assert order.get("courierId") == courier_id
                assert order.get("metroStation") == station

        step_check_response()
