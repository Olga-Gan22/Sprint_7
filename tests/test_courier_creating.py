"""Создание курьера"""

import allure
import requests
from data.creating_data import Url, ResponseMesseges
from helpers import get_courier_payload  # <-- добавили этот импорт


class TestCreatingCourier:

    @allure.feature("Couriers API")
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера: статус 201 и ok=true")
    def test_create_courier_success(self, created_courier):
        response = created_courier["response"]
        payload = created_courier["payload"]

        @allure.step("Проверяем статус 201")
        def step_check_status():
            assert response.status_code == 201, (
                f"Ожидался статус 201, но получен {response.status_code}. "
                f"Тело: {response.text}"
            )

        @allure.step("Проверяем поле 'ok': должно быть true")
        def step_check_ok():
            body = response.json()
            assert "ok" in body, "В ответе отсутствует поле 'ok'"
            assert body["ok"] is True, f"Поле 'ok' не равно true. Получено: {body['ok']}"

        step_check_status()
        step_check_ok()

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

        @allure.step(f"Попытка создать курьера с существующим логином: {existing_login}")
        def step_send_duplicate():
            return requests.post(
                f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
                json=duplicate_payload,
                headers={"Content-Type": "application/json"},
            )

        @allure.step("Проверка ответа: статус 409 и корректное сообщение")
        def step_verify_error(resp):
            assert resp.status_code == 409, (
                f"Ожидался статус 409 Conflict, но получен {resp.status_code}"
            )
            body = resp.json()
            assert "message" in body, "В ответе нет поля 'message'"
            assert (
                body["message"] == ResponseMesseges.COURIER_CREATED_FAILURE_DUPLICATE_LOGIN
            ), f"Неверное сообщение. Получено: {body['message']}"

        response = step_send_duplicate()
        step_verify_error(response)

    @allure.feature("Couriers API")
    @allure.story("Создание курьера")
    @allure.title("Отсутствие обязательных полей: статус 400 и сообщение об ошибке")
    def test_missing_required_fields(self):  # <-- убрали courier_payload из аргументов
        # Берем данные напрямую из helpers, чтобы не зависеть от фикстуры
        base_payload = get_courier_payload()
        bad_payload = {"login": base_payload["login"]}  # Только логин, остальное удаляем

        @allure.step("Отправка запроса без password и firstName")
        def step_send_bad():
            return requests.post(
                f"{Url.MAIN_URL}{Url.CREATING_COURIER}",
                json=bad_payload,
                headers={"Content-Type": "application/json"},
            )

        @allure.step("Проверка ответа: статус 400 и сообщение")
        def step_verify_bad(resp):
            assert resp.status_code == 400, (
                f"Ожидался статус 400 Bad Request, но получен {resp.status_code}"
            )
            body = resp.json()
            assert "message" in body, "В ответе нет поля 'message'"
            assert (
                body["message"] == ResponseMesseges.COURIER_CREATED_WITHOUT_DATA
            ), f"Неверное сообщение. Получено: {body['message']}"

        response = step_send_bad()
        step_verify_bad(response)
