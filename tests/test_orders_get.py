import requests
import pytest
import allure
from data.creating_data import Url


@allure.title("Успешное получение заказа по track: 200 + объект заказа")
def test_get_order_success(courier_with_order):
    order_id = courier_with_order["order_id"]  

    url = f"{Url.MAIN_URL}/api/v1/orders/track"
    params = {"t": order_id}

    resp = requests.get(url, params=params)

    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
    body = resp.json()

    assert "order" in body, f"В ответе нет поля 'order'. Ответ: {body}"
    assert body["order"].get("track") == int(order_id), (
        f"Track в ответе не совпадает с запрошенным. Ожидался {order_id}, получен {body['order'].get('track')}"
    )


@allure.title("Ошибка при запросе заказа без параметра t: 400 + сообщение")
def test_get_order_without_track(courier_with_order):
    url = f"{Url.MAIN_URL}/api/v1/orders/track"

    resp = requests.get(url)

    assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
    body = resp.json()
    assert body.get("message") == "Недостаточно данных для поиска", (
        f"Ожидается сообщение 'Недостаточно данных для поиска', получено: {body.get('message')}"
    )


@allure.title("Ошибка при запросе несуществующего заказа: 404 + сообщение")
def test_get_order_invalid_track(courier_with_order):
    invalid_track = "999999"  

    url = f"{Url.MAIN_URL}/api/v1/orders/track"
    params = {"t": invalid_track}

    resp = requests.get(url, params=params)

    assert resp.status_code == 404, f"Ожидался 404, получен {resp.status_code}"
    body = resp.json()
    assert body.get("message") == "Заказ не найден", (
        f"Ожидается сообщение 'Заказ не найден', получено: {body.get('message')}"
    )
