import pytest
import requests
import time
from generators import (
    firstName_generator,
    lastName_generator,
    address_generator,
    phone_generator,
    metro_station_generator,
    rent_time_generator,
    login_generator,
    password_generator
)
from data.creating_data import Url, ResponseMesseges, Colors

"""создание курьера"""
@pytest.fixture
def courier_payload():
    
    return {
        "login": login_generator(),
        "password": password_generator(),
        "firstName": firstName_generator(),
    }


@pytest.fixture
def created_courier():
   
    payload = {
        "login": login_generator(),
        "password": password_generator(),
        "firstName": firstName_generator(),
    }
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
        json=payload,
    )
    assert response.status_code == 201, (
        f"Не удалось создать курьера. Ожидался 201, получен {response.status_code}. Тело: {response.text}"
    )

    time.sleep(2)

    return {"payload": payload, "response": response}

"""логин курьера"""
@pytest.fixture
def logged_in_courier(created_courier):

    payload = created_courier["payload"]
    login_payload = {
        "login": payload["login"],
        "password": payload["password"],
    }

    login_response = requests.post(
        f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
        json=login_payload,
    )

    assert login_response.status_code == 200, (
        f"Не удалось залогинить курьера. Ожидался 200, получен {login_response.status_code}. Тело: {login_response.text}"
    )
    body = login_response.json()
    assert "id" in body, "В ответе на успешный логин нет поля 'id'"

    return {
        "payload": payload,
        "login_response": login_response,
        "courier_id": body["id"],
    }


@pytest.fixture
def create_order(color_value):
    """
    Фикстура для создания заказа.
    Принимает color_value напрямую (None или список цветов).
    Явно добавляет его в payload.
    """
       # Базовый payload
    payload = {
        "firstName": firstName_generator(),
        "lastName": lastName_generator(),
        "address": address_generator(),
        "metroStation": metro_station_generator(),
        "phone": phone_generator(),
        "rentTime": rent_time_generator(),
        "deliveryDate": "2024-12-20",
        "comment": "Test order comment",
    }

    # Явно добавляем цвет, если он передан
    if color_value is not None:
        payload["color"] = color_value

    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201, (
        f"Не удалось создать заказ. Ожидался 201, получен {response.status_code}. Тело: {response.text}"
    )

    return {"response": response, "payload": payload}

@pytest.fixture
def courier_with_order():
    # SETUP

    # 1. Создаём курьера
    login = login_generator()
    password = password_generator()

    payload_courier = {
        "login": login,
        "password": password,
        "firstName": firstName_generator(),
        "lastName": lastName_generator(),
    }

    resp_create = requests.post(
        f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
        json=payload_courier,
    )
    assert resp_create.status_code == 201, (
        f"[Создание курьера] Ожидался 201, получен {resp_create.status_code}: {resp_create.text}"
    )

    # 2. Логиним курьера, чтобы получить courier_id
    payload_login = {
        "login": login,
        "password": password,
    }
    resp_login = requests.post(
        f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
        json=payload_login,
    )
    assert resp_login.status_code == 200, (
        f"[Логин курьера] Ожидался 200, получен {resp_login.status_code}: {resp_login.text}"
    )

    login_body = resp_login.json()
    assert "id" in login_body, f"В ответе на логин нет поля 'id'. Ответ: {login_body}"
    courier_id = login_body["id"]

    # 3. Создаём заказ
    payload_order = {
        "courierId": courier_id,
        "firstName": firstName_generator(),
        "lastName": lastName_generator(),
        "address": address_generator(),
        "metroStation": metro_station_generator(),
        "phone": phone_generator(),
        "rentTime": rent_time_generator(),
        "deliveryDate": "2024-11-05",
    }

    resp_order = requests.post(
        f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
        json=payload_order,
    )
    assert resp_order.status_code in [200, 201], (
        f"[Создание заказа] Ожидался 200/201, получен {resp_order.status_code}: {resp_order.text}"
    )

    order_body = resp_order.json()
    assert "track" in order_body, f"В ответе на создание заказа нет поля 'track'. Ответ: {order_body}"

    # ВАЖНО: приводим track к строке — это частая причина 404
    order_track = str(order_body["track"])

    yield {"courier_id": courier_id, "order_id": order_track}

    # Teardown
    requests.delete(
        f"{Url.MAIN_URL}{Url.COURIER_DELETE.format(courier_id=courier_id)}"
    )