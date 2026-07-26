import pytest
import requests
from data.creating_data import Url
from helpers import get_courier_payload, get_full_courier_payload, get_order_payload

@pytest.fixture
def courier_payload():
   
    return get_courier_payload()


@pytest.fixture
def created_courier():
    
    payload = get_courier_payload()
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
        json=payload,
    )
    return {"payload": payload, "response": response}


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
    body = login_response.json()
    courier_id = body.get("id")  # Может быть None, если логин не удался

    return {
        "payload": payload,
        "login_response": login_response,
        "courier_id": courier_id,
    }


@pytest.fixture
def create_order():
    """
    Фикстура для создания заказа БЕЗ цвета (color_value=None).
    Никаких assert внутри!
    """
    payload = get_order_payload(color_value=None)
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    # Assert убран! Проверки будут в тестах
    return {"response": response, "payload": payload}


@pytest.fixture
def create_order_with_color(color_value):
    """
    Фикстура для создания заказа С цветом.
    color_value передаётся через параметризацию теста.
    Никаких assert внутри!
    """
    payload = get_order_payload(color_value)
    response = requests.post(
        f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    # Assert убран!
    return {"response": response, "payload": payload}

@pytest.fixture
def courier_with_order():
   
    # 1. Создать курьера (используем полную версию, т.к. там lastName)
    payload_courier = get_full_courier_payload()
    resp_create = requests.post(
        f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
        json=payload_courier,
    )

    # 2. Авторизовать курьера
    payload_login = {
        "login": payload_courier["login"],
        "password": payload_courier["password"],
    }
    resp_login = requests.post(
        f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
        json=payload_login,
    )
    login_body = resp_login.json()
    courier_id = login_body.get("id")

    order_track = None
    resp_order = None

    if courier_id is not None:
        # 3. Создать заказ
        payload_order = get_order_payload()  # можно передать color_value, если нужно
        payload_order["courierId"] = courier_id

        resp_order = requests.post(
            f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
            json=payload_order,
        )
        order_body = resp_order.json() if resp_order else {}
        order_track = str(order_body.get("track", ""))

    yield {
        "courier_id": courier_id,
        "order_id": order_track,
        "resp_create_courier": resp_create,
        "resp_login": resp_login,
        "resp_order": resp_order,
    }

    # Teardown: удалить курьера после теста (это правильно и должно быть здесь)
    if courier_id is not None:
        requests.delete(
            f"{Url.MAIN_URL}{Url.COURIER_DELETE.format(courier_id=courier_id)}"
        )
