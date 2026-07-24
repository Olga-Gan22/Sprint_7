import requests
import pytest
import allure
from data.creating_data import Url


@allure.title("Успешное принятие заказа: 200 + ok=true")
def test_accept_order_success(courier_with_order):
    courier_id = courier_with_order["courier_id"]
    order_id = courier_with_order["order_id"]  # это track

    url = f"{Url.MAIN_URL}{Url.ORDERS_ACCEPT.format(id=order_id)}?courierId={courier_id}"
    resp = requests.put(url)

    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
    body = resp.json()
    assert body.get("ok") is True, f"Ожидается ok=True, получено: {body}"


@allure.title("Ошибка при принятии заказа без courierId")
def test_accept_without_courier_id(courier_with_order):
    order_id = courier_with_order["order_id"]

    url = f"{Url.MAIN_URL}/api/v1/orders/accept/{order_id}"
    resp = requests.put(url)

    assert resp.status_code in [400, 422, 500], f"Ожидалась ошибка, получен {resp.status_code}"


@allure.title("Ошибка при принятии заказа с несуществующим courierId")
def test_accept_with_invalid_courier_id(courier_with_order):
    order_id = courier_with_order["order_id"]
    invalid_courier_id = 999999

    url = f"{Url.MAIN_URL}{Url.ORDERS_ACCEPT.format(id=order_id)}?courierId={invalid_courier_id}"
    resp = requests.put(url)

    assert resp.status_code in [404, 400], f"Ожидалась ошибка (404/400), получен {resp.status_code}"


@allure.title("Ошибка при отсутствии ID заказа в URL (не подставлен track)")
def test_accept_without_order_id(courier_with_order):
    courier_id = courier_with_order["courier_id"]

    base_url = f"{Url.MAIN_URL}/api/v1/orders/accept?courierId={courier_id}"
    resp = requests.put(base_url)

    assert resp.status_code in [404, 400], f"Ожидалась ошибка (404/400), получен {resp.status_code}"


@allure.title("Ошибка при принятии несуществующего заказа (неверный track)")
def test_accept_with_invalid_order_id(courier_with_order):
    courier_id = courier_with_order["courier_id"]
    invalid_order_id = 999999  # несуществующий track

    url = f"{Url.MAIN_URL}{Url.ORDERS_ACCEPT.format(id=invalid_order_id)}?courierId={courier_id}"
    resp = requests.put(url)

    assert resp.status_code in [404, 400], f"Ожидалась ошибка (404/400), получен {resp.status_code}"
