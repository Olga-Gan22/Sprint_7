"""логин курьера"""


import time
import requests
import allure
from data.creating_data import Url, ResponseMesseges
from conftest import courier_payload, created_courier, logged_in_courier


class TestCourierLogin:

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Успешная авторизация: статус 200 и наличие id")
    def test_successful_login(self, logged_in_courier):
        response = logged_in_courier["login_response"]
        body = response.json()

        assert response.status_code == 200
        assert "id" in body
        assert isinstance(body["id"], int)

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Отсутствие обязательных полей при логине: статус 400")
    def test_login_without_required_fields(self, courier_payload):
        
        payload_missing = {
            "login": courier_payload["login"],
        }

        headers = {"Content-Type": "application/json"}
        time.sleep(3)

        response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=payload_missing,
            headers=headers,
        )

        assert response.status_code == 400, f"Ожидался 400, но получен {response.status_code}. Тело: {response.text}"
        body = response.json()
        assert "message" in body, "В ответе нет поля 'message'"
        assert body["message"] == ResponseMesseges.LOGIN_WITHOUT_DATA

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Неверная пара логин-пароль: статус 404")
    def test_login_with_wrong_password(self, created_courier):
        payload = created_courier["payload"]

        wrong_payload = {
            "login": payload["login"],
            "password": "wrong_password_123",  # заведомо неверный пароль
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=wrong_payload,
            headers=headers,
        )

        assert response.status_code == 404, f"Ожидался 404, но получен {response.status_code}"
        body = response.json()
        assert "message" in body
        assert body["message"] == ResponseMesseges.LOGIN_NOT_FOUND

    @allure.feature("Couriers API")
    @allure.story("Авторизация курьера")
    @allure.title("Логин под несуществующим пользователем: статус 404")
    def test_login_non_existent_user(self):
        non_existent_payload = {
            "login": "non_existent_login_999",
            "password": "any_password_123"
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=non_existent_payload,
            headers=headers,
        )

        assert response.status_code == 404, f"Ожидался 404, но получен {response.status_code}"
        body = response.json()
        assert "message" in body
        assert body["message"] == ResponseMesseges.LOGIN_NOT_FOUND
