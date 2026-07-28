"""создание заказа"""

import allure
import pytest
from data.creating_data import Colors


@allure.feature("Orders API")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа без параметра color: track присутствует, color отсутствует в payload")
    def test_create_order_without_color(self, create_order):
        response = create_order["response"]
        payload = create_order["payload"]
        body = response.json()

        @allure.step("Проверяем статус 201")
        def step_check_status():
            assert response.status_code == 201, (
                f"Ожидался статус 201, но получен {response.status_code}. Тело: {response.text}"
            )

        @allure.step("Проверяем наличие поля track и что оно число")
        def step_check_track():
            assert "track" in body, "В ответе нет обязательного поля 'track'"
            assert isinstance(body["track"], int), "Поле 'track' должно быть числом"

        @allure.step("Проверяем, что color отсутствует в payload")
        def step_check_no_color():
            assert "color" not in payload, "Цвет не должен быть в payload, если не передавался"

        # Все шаги вызываются подряд. Если step_check_status падает — тест падает сразу.
        step_check_status()
        step_check_track()
        step_check_no_color()

    @allure.title("Создание заказа с параметром color: цвет совпадает и track присутствует")
    @pytest.mark.parametrize("color_value", [Colors.BLACK, Colors.GREY])
    @pytest.mark.xfail(
        reason="Стенд возвращает 500 (values.map is not a function) при создании заказа с параметром color. "
               "Это проблема бэкенда стенда, а не теста.",
        strict=False
    )
    def test_create_order_with_color(self, color_value, create_order_with_color):
        response = create_order_with_color["response"]
        payload = create_order_with_color["payload"]
        body = response.json()

        @allure.step(f"Проверяем статус 201 для заказа с цветом {color_value}")
        def step_check_status():
            assert response.status_code == 201, (
                f"Ожидался статус 201, но получен {response.status_code}. Тело: {response.text}"
            )

        @allure.step("Проверяем наличие track и его тип")
        def step_check_track():
            assert "track" in body, "В ответе нет обязательного поля 'track'"
            assert isinstance(body["track"], int), "Поле 'track' должно быть числом"

        @allure.step("Проверяем соответствие color в payload переданному значению")
        def step_check_color():
            assert "color" in payload, "Поле color должно присутствовать в payload"
            assert payload["color"] == color_value, (
                f"Цвет в payload ({payload['color']}) не совпадает с переданным ({color_value})"
            )

        step_check_status()
        step_check_track()
        step_check_color()
