"""создание заказа"""

import allure
import pytest
from data.creating_data import Colors

@allure.feature("Orders API")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа: проверка поля track и вариаций цвета")
    @pytest.mark.parametrize("color_value", [
        None,
        [Colors.BLACK],
        [Colors.GREY],
        [Colors.BLACK, Colors.GREY],
    ])
    def test_create_order_with_color_variations(self, create_order, color_value):
        response = create_order["response"]
        body = response.json()

        assert response.status_code == 201, f"Ожидался 201, но получен {response.status_code}"
        assert "track" in body, "В ответе нет обязательного поля 'track'"
        assert isinstance(body["track"], int), "Поле 'track' должно быть числом"

        if color_value is not None:
           
            assert "color" in create_order["payload"], "Цвет должен быть в payload, если передан"
            assert create_order["payload"]["color"] == color_value, "Цвет в payload не совпадает с переданным"
        else:
            assert "color" not in create_order["payload"], "Цвет не должен быть в payload, если не передан"
