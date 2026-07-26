import requests
import pytest
import allure
from data.creating_data import Url


@allure.feature("Orders API")
@allure.story("Получение заказа по track")
@allure.title("Успешное получение заказа по track: 200 + объект заказа")
def test_get_order_success(courier_with_order):
    order_id = courier_with_order["order_id"]

    @allure.step("Формируем URL и параметры запроса: t = track заказа")
    def step_build_request():
        url = f"{Url.MAIN_URL}/api/v1/orders/track"
        params = {"t": order_id}
        return url, params

    url, params = step_build_request()

    @allure.step("Отправляем GET-запрос для получения заказа по track")
    def step_send_request():
        return requests.get(url, params=params)

    resp = step_send_request()

    @allure.step("Проверяем, что статус ответа равен 200")
    def step_check_status():
        assert resp.status_code == 200, (
            f"Ожидался статус 200, но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()

    body = resp.json()

    @allure.step("Проверяем наличие поля 'order' в ответе")
    def step_check_order_field():
        assert "order" in body, (
            f"В ответе отсутствует поле 'order'. Полученный JSON: {body}"
        )

    step_check_order_field()

    @allure.step("Проверяем совпадение track в ответе с запрошенным track")
    def step_check_track_match():
        order_body = body["order"]
        track_in_response = order_body.get("track")

        # Приводим к строке для безопасного сравнения (на случай, если API отдаёт track как строку/число)
        assert str(track_in_response) == str(order_id), (
            f"Track в ответе не совпадает с запрошенным. Ожидался {order_id}, "
            f"получен {track_in_response}. Ответ: {body}"
        )

    step_check_track_match()


@allure.feature("Orders API")
@allure.story("Получение заказа по track")
@allure.title("Ошибка при запросе заказа без параметра t: 400 + сообщение")
def test_get_order_without_track(courier_with_order):
    url = f"{Url.MAIN_URL}/api/v1/orders/track"

    @allure.step("Отправляем GET-запрос без параметра t")
    def step_send_request():
        return requests.get(url)

    resp = step_send_request()

    @allure.step("Проверяем, что статус ответа равен 400")
    def step_check_status():
        assert resp.status_code == 400, (
            f"Ожидался статус 400, но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()

    body = resp.json()

    @allure.step("Проверяем точное сообщение об ошибке в теле ответа")
    def step_check_message():
        expected_message = "Недостаточно данных для поиска"
        actual_message = body.get("message")
        assert actual_message == expected_message, (
            f"Ожидается сообщение '{expected_message}', но получено: '{actual_message}'. "
            f"Полный ответ: {body}"
        )

    step_check_message()


@allure.feature("Orders API")
@allure.story("Получение заказа по track")
@allure.title("Ошибка при запросе несуществующего заказа: 404 + сообщение")
def test_get_order_invalid_track(courier_with_order):
    invalid_track = "999999"
    url = f"{Url.MAIN_URL}/api/v1/orders/track"
    params = {"t": invalid_track}

    @allure.step("Отправляем GET-запрос с несуществующим track")
    def step_send_request():
        return requests.get(url, params=params)

    resp = step_send_request()

    @allure.step("Проверяем, что статус ответа равен 404")
    def step_check_status():
        assert resp.status_code == 404, (
            f"Ожидался статус 404, но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()

    body = resp.json()

    @allure.step("Проверяем точное сообщение об ошибке 'Заказ не найден'")
    def step_check_message():
        expected_message = "Заказ не найден"
        actual_message = body.get("message")
        assert actual_message == expected_message, (
            f"Ожидается сообщение '{expected_message}', но получено: '{actual_message}'. "
            f"Полный ответ: {body}"
        )

    step_check_message()
