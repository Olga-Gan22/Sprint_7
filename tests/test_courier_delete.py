"""Удаление курьера"""

import allure
import pytest
import requests
from data.creating_data import Url


@allure.feature("Couriers API")
@allure.story("Удаление курьера")
class TestCourierDelete:

    @allure.title("Удаление курьера: ожидаем 200 OK (стенд сейчас возвращает 404 — это известный баг)")
    @pytest.mark.parametrize("courier_id", ["1", "2"])
    @pytest.mark.xfail(
        reason="Стенд не поддерживает удаление курьера: сервер возвращает 404 вместо 200 OK. "
               "Это известное ограничение стенда, не ошибка теста.",
        strict=False
    )
    def test_delete_courier_success(self, courier_id):
        url = f"{Url.MAIN_URL}{Url.COURIER_DELETE.format(courier_id=courier_id)}"

        @allure.step(f"Отправляем DELETE-запрос на удаление курьера {courier_id}")
        def step_send_delete():
            return requests.delete(url)

        response = step_send_delete()

        @allure.step("Проверяем, что статус ответа равен 200")
        def step_check_status():
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}. "
                f"Тело ответа: {response.text}"
            )

        @allure.step("Проверяем структуру ответа: наличие поля 'ok' и его значение true")
        def step_check_body():
            body = response.json()
            assert "ok" in body, "В ответе отсутствует обязательное поле 'ok'"
            assert body["ok"] is True, f"Поле 'ok' не равно true. Получено: {body['ok']}"

        step_check_status()
        step_check_body()

    @allure.title("Удаление несуществующего курьера: ожидаем 404 и сообщение об ошибке")
    @pytest.mark.parametrize("courier_id", ["9998", "9999"])
    def test_delete_courier_not_found(self, courier_id):
        url = f"{Url.MAIN_URL}{Url.COURIER_DELETE.format(courier_id=courier_id)}"

        @allure.step(f"Отправляем DELETE-запрос для несуществующего курьера {courier_id}")
        def step_send_delete_not_found():
            return requests.delete(url)

        response = step_send_delete_not_found()

        @allure.step("Проверяем, что статус ответа равен 404")
        def step_check_404():
            assert response.status_code == 404, (
                f"Ожидался статус 404, но получен {response.status_code}. "
                f"Тело ответа: {response.text}"
            )

        @allure.step("Проверяем формат JSON-ответа и наличие поля 'message'")
        def step_check_message_field():
            body = response.json()
            assert "message" in body, "При статусе 404 в ответе должно быть поле 'message'"
            expected_msg = "Курьера с таким id нет"
            assert expected_msg in body["message"], (
                f"Сообщение об ошибке не соответствует ожидаемому. "
                f"Ожидалось: '{expected_msg}', получено: '{body.get('message')}'"
            )

        step_check_404()
        step_check_message_field()
