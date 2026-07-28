# tests/test_orders_get.py

import allure
import requests
import pytest
from data.creating_data import Url


@allure.feature("Orders API")
@allure.story("Получение заказа по track")
@allure.title("Успешное получение заказа по track: 200 + объект заказа")
def test_get_order_success(create_order):
    with allure.step("Получаем JSON-ответ от создания заказа"):
        order_body = create_order["response"].json()

    order_id = order_body.get("track")
    assert order_id is not None, "Не удалось получить track заказа из ответа"

    @allure.step("Формируем URL и параметры запроса: t = track заказа")
    def step_build_request():
        url = f"{Url.MAIN_URL}/api/v1/orders/track"
        params = {"t": order_id}
        return url, params

    url, params = step_build_request()

    @allure.step("Отправляем GET-запрос для получения заказа по track")
    def step_send_request():
        return requests.get(url, params=params, headers={"Content-Type": "application/json"})

    resp = step_send_request()

    @allure.step("Проверяем, что статус ответа равен 200")
    def step_check_status():
        assert resp.status_code == 200, (
            f"Ожидался статус 200, но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()

    @allure.step("Проверяем, что в ответе есть объект заказа")
    def step_check_body():
        body = resp.json()
        assert isinstance(body, dict), "Ответ должен быть JSON-объектом"

    step_check_body()
