"""Логика генерации данных"""

from generators import (
    firstName_generator,
    lastName_generator,
    address_generator,
    phone_generator,
    metro_station_generator,
    rent_time_generator,
    login_generator,
    password_generator,
)
"""Создание курьера"""
def get_courier_payload():
   
    return {
        "login": login_generator(),
        "password": password_generator(),
        "firstName": firstName_generator(),
    }

"""Полный payload для курьера"""
def get_full_courier_payload():
   
    return {
        "login": login_generator(),
        "password": password_generator(),
        "firstName": firstName_generator(),
        "lastName": lastName_generator(),
    }

"""Payload для создания заказа"""
def get_order_payload(color_value=None):

    payload = {
        "firstName": firstName_generator(),
        "lastName": lastName_generator(),
        "address": address_generator(),
        "metroStation": metro_station_generator(),
        "phone": phone_generator(),
        "rentTime": rent_time_generator(),
        "deliveryDate": "2024-12-20",
        "comment": "Test order comment",
    }

    if color_value is not None:
        payload["color"] = color_value

    return payload

