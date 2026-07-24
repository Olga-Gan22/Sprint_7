"""Создание курьера"""

import requests
import allure
from data.creating_data import Url, ResponseMesseges
from conftest import courier_payload, created_courier


class TestCreatingCourier:

    @allure.feature("Couriers API")
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера: статус 201 и ok=true")
    def test_create_courier_success(self, courier_payload):
        response = requests.post(
            f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
            json=courier_payload,
        )

        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}. Тело: {response.text}"
        body = response.json()
        assert "ok" in body, "В ответе отсутствует поле 'ok'"
        assert body["ok"] is True, f"Поле 'ok' не равно true. Получено: {body['ok']}"

    @allure.feature("Couriers API")
    @allure.story("Создание курьера")
    @allure.title("Дубликат логина: статус 409 и сообщение об ошибке")
    def test_cannot_create_duplicate_login(self, created_courier):
        existing_login = created_courier["payload"]["login"]

        duplicate_payload = {
            "login": existing_login,
            "password": "another_password_123",
            "firstName": "Another Name",
        }

        response = requests.post(
            f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
            json=duplicate_payload,
        )

        assert response.status_code == 409, f"Ожидался статус 409 Conflict, но получен {response.status_code}"
        body = response.json()
        assert "message" in body, "В ответе на конфликт логина нет поля 'message'"
        assert body["message"] == ResponseMesseges.COURIER_CREATED_FAILURE_DUPLICATE_LOGIN

    @allure.feature("Couriers API")
    @allure.story("Создание курьера")
    @allure.title("Отсутствие обязательных полей: статус 400 и сообщение об ошибке")
    def test_missing_required_fields(self, courier_payload):
        payload_missing = {
            "login": courier_payload["login"],
            # password и firstName намеренно не передаём
        }

        response = requests.post(
            f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
            json=payload_missing,
        )

        assert response.status_code == 400, f"Ожидался статус 400 Bad Request, но получен {response.status_code}"
        body = response.json()
        assert "message" in body, "В ответе при ошибке нет поля 'message'"
        assert body["message"] == ResponseMesseges.COURIER_CREATED_WITHOUT_DATA
