import pytest
import requests
from data.creating_data import Url
from helpers import (
    get_full_courier_payload,
    get_order_payload,
)

@pytest.fixture
def created_courier():
    payload = get_full_courier_payload()
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return {"payload": payload, "response": response}


@pytest.fixture
def logged_in_courier(created_courier):
    """    Только авторизует курьера.     """
    payload = created_courier["payload"]
    login_payload = {
        "login": payload["login"],
        "password": payload["password"],
    }

    login_response = requests.post(
        f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
        json=login_payload,
        headers={"Content-Type": "application/json"},
    )

    body = login_response.json()
    courier_id = body.get("id")

    return {
        "payload": payload,
        "login_response": login_response,
        "courier_id": courier_id,
    }


@pytest.fixture
def create_order():
    """Только создаёт заказ без цвета. Возвращает response и payload."""
    payload = get_order_payload(color_value=None)
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return {"response": response, "payload": payload}


@pytest.fixture
def create_order_with_color(color_value):
    """Создаёт заказ с цветом. color_value передаётся из теста."""
    payload = get_order_payload(color_value)
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return {"response": response, "payload": payload}


@pytest.fixture
def courier_with_order():
    """    Составная фикстура для позитивных тестов    """
    # Шаг 1: создать курьера
    payload_courier = get_full_courier_payload()
    resp_create = requests.post(
        f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
        json=payload_courier,
        headers={"Content-Type": "application/json"},
    )
    create_body = resp_create.json()
    courier_id = create_body.get("id")

    order_track = None
    resp_order = None
    resp_login = None

    # Шаг 2: авторизовать курьера
    if courier_id:
        payload_login = {
            "login": payload_courier["login"],
            "password": payload_courier["password"],
        }
        resp_login = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=payload_login,
            headers={"Content-Type": "application/json"},
        )
        login_body = resp_login.json()
        final_courier_id = login_body.get("id", courier_id)

        # Шаг 3: создать заказ
        if final_courier_id:
            payload_order = get_order_payload()
            resp_order = requests.post(
                f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
                json=payload_order,
                headers={"Content-Type": "application/json"},
            )
            order_body = resp_order.json()
            order_track = str(order_body.get("track", ""))

    result = {
        "courier_id": final_courier_id if courier_id else courier_id,
        "order_id": order_track,
        "resp_create_courier": resp_create,
        "resp_login": resp_login,
        "resp_order": resp_order,
    }

    yield result

    if courier_id:
        requests.delete(
            f"{Url.MAIN_URL}{Url.COURIER_DELETE.format(courier_id=courier_id)}",
            headers={"Content-Type": "application/json"},
            timeout=10,
        )