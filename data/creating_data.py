class Url:
    MAIN_URL = "https://qa-scooter.praktikum-services.ru"
    CREATING_COURIER = "/api/v1/courier"
    LOGIN_COURIER = "/api/v1/courier/login"
    CREATE_ORDER = "/api/v1/orders"
    ORDERS = "/api/v1/orders"
    COURIER_DELETE = "/api/v1/courier/{courier_id}"
    ORDERS_ACCEPT = "/api/v1/orders/accept/{id}"

class ResponseMesseges:
    # Для создания курьера
    COURIER_CREATED_FAILURE_DUPLICATE_LOGIN = "Этот логин уже используется. Попробуйте другой."
    COURIER_CREATED_WITHOUT_DATA = "Недостаточно данных для создания учетной записи"

    # Для логина курьера
    LOGIN_WITHOUT_DATA = "Недостаточно данных для входа"
    LOGIN_NOT_FOUND = "Учетная запись не найдена"

class Colors:
    BLACK = "BLACK"
    GREY = "GREY"
