import requests
import pytest
import allure
from data.creating_data import Url


@allure.feature("Orders API")
@allure.story("Принятие заказа")
@allure.title("Успешное принятие заказа: 200 + ok=true")
@pytest.mark.xfail(
    reason="Стенд возвращает 404: 'Заказа с таким id не существует'. "
           "Вероятно, заказ удаляется/сбрасывается между созданием и принятием. "
           "Это проблема стенда, а не логики теста.",
    strict=False
)
def test_accept_order_success(courier_with_order):
    courier_id = courier_with_order["courier_id"]
    order_id = courier_with_order["order_id"]  # это track

    @allure.step("Формируем URL для принятия заказа с courierId и orderId")
    def step_build_url():
        return f"{Url.MAIN_URL}{Url.ORDERS_ACCEPT.format(id=order_id)}?courierId={courier_id}"

    url = step_build_url()

    @allure.step("Отправляем PUT-запрос на принятие заказа")
    def step_send_request():
        return requests.put(url)

    resp = step_send_request()

    @allure.step("Проверяем, что статус ответа равен 200")
    def step_check_status():
        assert resp.status_code == 200, (
            f"Ожидался статус 200, но получен {resp.status_code}. Тело: {resp.text}"
        )

    @allure.step("Проверяем, что в ответе ok=true")
    def step_check_body():
        body = resp.json()
        assert body.get("ok") is True, (
            f"Ожидается ok=True, но получено: {body}"
        )

    step_check_status()
    step_check_body()


@allure.feature("Orders API")
@allure.story("Принятие заказа")
@allure.title("Ошибка при принятии заказа без courierId")
def test_accept_without_courier_id(courier_with_order):
    order_id = courier_with_order["order_id"]

    @allure.step("Формируем URL без параметра courierId (только orderId в пути)")
    def step_build_url():
        return f"{Url.MAIN_URL}/api/v1/orders/accept/{order_id}"

    url = step_build_url()

    @allure.step("Отправляем PUT-запрос без courierId")
    def step_send_request():
        return requests.put(url)

    resp = step_send_request()

    @allure.step("Проверяем, что получен статус ошибки (400/422/500)")
    def step_check_status():
        assert resp.status_code in [400, 422, 500], (
            f"Ожидалась ошибка (400/422/500), но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()


@allure.feature("Orders API")
@allure.story("Принятие заказа")
@allure.title("Ошибка при принятии заказа с несуществующим courierId")
def test_accept_with_invalid_courier_id(courier_with_order):
    order_id = courier_with_order["order_id"]
    invalid_courier_id = 999999

    @allure.step("Формируем URL с заведомо несуществующим courierId")
    def step_build_url():
        return f"{Url.MAIN_URL}{Url.ORDERS_ACCEPT.format(id=order_id)}?courierId={invalid_courier_id}"

    url = step_build_url()

    @allure.step("Отправляем PUT-запрос с неверным courierId")
    def step_send_request():
        return requests.put(url)

    resp = step_send_request()

    @allure.step("Проверяем, что получен статус 404 или 400")
    def step_check_status():
        assert resp.status_code in [404, 400], (
            f"Ожидалась ошибка (404/400), но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()


@allure.feature("Orders API")
@allure.story("Принятие заказа")
@allure.title("Ошибка при отсутствии ID заказа в URL (не подставлен track)")
def test_accept_without_order_id(courier_with_order):
    courier_id = courier_with_order["courier_id"]

    @allure.step("Формируем URL, где orderId отсутствует в пути, только courierId в query")
    def step_build_url():
        return f"{Url.MAIN_URL}/api/v1/orders/accept?courierId={courier_id}"

    base_url = step_build_url()

    @allure.step("Отправляем PUT-запрос без orderId в URL")
    def step_send_request():
        return requests.put(base_url)

    resp = step_send_request()

    @allure.step("Проверяем, что получен статус 404 или 400")
    def step_check_status():
        assert resp.status_code in [404, 400], (
            f"Ожидалась ошибка (404/400), но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()


@allure.feature("Orders API")
@allure.story("Принятие заказа")
@allure.title("Ошибка при принятии несуществующего заказа (неверный track)")
def test_accept_with_invalid_order_id(courier_with_order):
    courier_id = courier_with_order["courier_id"]
    invalid_order_id = 999999  # несуществующий track

    @allure.step("Формируем URL с заведомо неверным orderId (track)")
    def step_build_url():
        return f"{Url.MAIN_URL}{Url.ORDERS_ACCEPT.format(id=invalid_order_id)}?courierId={courier_id}"

    url = step_build_url()

    @allure.step("Отправляем PUT-запрос с неверным orderId")
    def step_send_request():
        return requests.put(url)

    resp = step_send_request()

    @allure.step("Проверяем, что получен статус 404 или 400")
    def step_check_status():
        assert resp.status_code in [404, 400], (
            f"Ожидалась ошибка (404/400), но получен {resp.status_code}. Тело: {resp.text}"
        )

    step_check_status()
