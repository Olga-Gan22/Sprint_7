from faker import Faker
import random

fake = Faker()

def login_generator():
    """Генерирует гарантированно уникальный логин для API-теста."""
    return f"{fake.user_name()}{random.randint(1000, 9999)}"

def password_generator():
    return fake.password()

def firstName_generator():
    return fake.first_name()

def lastName_generator():
    return fake.last_name()

def address_generator():
    return f"{fake.street_address()}, apt. {random.randint(1, 200)}"

def phone_generator():
    digits = "".join([str(random.randint(0, 9)) for _ in range(10)])
    return f"+7 {digits[:3]} {digits[3:6]} {digits[6:8]} {digits[8:]}"

def metro_station_generator():
    return random.randint(1, 50)

def rent_time_generator():
    return random.randint(1, 7)