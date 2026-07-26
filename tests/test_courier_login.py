"""логин курьера"""

import requests
import allure
import pytest
from data.creating_data import Url, ResponseMesseges
from conftest import courier_payload, created_courier, logged_in_courier


class TestCourierLogin:

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Успешная авторизация: статус 200 и наличие id")
    def test_successful_login(self, logged_in_courier):
        response = logged_in_courier["login_response"]

        @allure.step("Проверяем статус ответа 200")
        def step_check_status():
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        @allure.step("Проверяем, что в ответе есть поле 'id' и оно типа int")
        def step_check_body():
            body = response.json()
            assert "id" in body, "В ответе нет поля 'id'"
            assert isinstance(body["id"], int), f"'id' должен быть числом, получен {type(body['id'])}"

        step_check_status()
        step_check_body()

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Отсутствие обязательных полей при логине: ожидаем 400 (стенд возвращает 504)")
    @pytest.mark.xfail(
        reason="Стенд стабильно возвращает 504 (таймаут) вместо 400 при отсутствии пароля. "
               "Это проблема стенда, а не логики теста.",
        strict=False
    )
    def test_login_without_required_fields(self, courier_payload):
        payload_missing = {
            "login": courier_payload["login"],
            # password намеренно не передаём
        }
        headers = {"Content-Type": "application/json"}

        @allure.step("Отправляем POST-запрос без поля password")
        def step_send_request():
            return requests.post(
                f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
                json=payload_missing,
                headers=headers,
            )

        response = step_send_request()

        @allure.step("Проверяем, что статус равен 400")
        def step_check_status():
            assert response.status_code == 400, (
                f"Ожидался 400, но получен {response.status_code}. Тело: {response.text}"
            )

        @allure.step("Проверяем наличие поля 'message' и его значение")
        def step_check_message():
            body = response.json()
            assert "message" in body, "В ответе нет поля 'message'"
            assert body["message"] == ResponseMesseges.LOGIN_WITHOUT_DATA

        step_check_status()
        step_check_message()

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Неверная пара логин-пароль: статус 404")
    def test_login_with_wrong_password(self, created_courier):
        payload = created_courier["payload"]
        wrong_payload = {
            "login": payload["login"],
            "password": "wrong_password_123",
        }
        headers = {"Content-Type": "application/json"}

        @allure.step("Отправляем POST с неверным паролем")
        def step_send_request():
            return requests.post(
                f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
                json=wrong_payload,
                headers=headers,
            )

        response = step_send_request()

        @allure.step("Проверяем, что статус равен 404")
        def step_check_status():
            assert response.status_code == 404, (
                f"Ожидался 404, но получен {response.status_code}"
            )

        @allure.step("Проверяем сообщение об ошибке")
        def step_check_message():
            body = response.json()
            assert "message" in body
            assert body["message"] == ResponseMesseges.LOGIN_NOT_FOUND

        step_check_status()
        step_check_message()

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Логин под несуществующим пользователем: статус 404")
    def test_login_non_existent_user(self):
        non_existent_payload = {
            "login": "non_existent_login_999",
            "password": "any_password_123"
        }
        headers = {"Content-Type": "application/json"}

        @allure.step("Отправляем POST для несуществующего пользователя")
        def step_send_request():
            return requests.post(
                f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
                json=non_existent_payload,
                headers=headers,
            )

        response = step_send_request()

        @allure.step("Проверяем, что статус равен 404")
        def step_check_status():
            assert response.status_code == 404, (
                f"Ожидался 404, но получен {response.status_code}"
            )

        @allure.step("Проверяем сообщение об ошибке")
        def step_check_message():
            body = response.json()
            assert "message" in body
            assert body["message"] == ResponseMesseges.LOGIN_NOT_FOUND

        step_check_status()
        step_check_message()
