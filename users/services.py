import time

import stripe
from config.settings import API_KEY_STRIPE


def get_link_to_payment(course_title: str, course_price: int) -> dict:
    """ Функция для получения ссылки на оплату"""

    stripe.api_key = API_KEY_STRIPE

    # Создаем продукт для оплаты
    product = stripe.Product.create(name=course_title)

    # Создаем цену для оплаты
    price = stripe.Price.create(
        currency="rub",
        unit_amount=course_price * 100,
        product_data={"name": product.get('id')},
    )

    # Создаем сессию для оплаты
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price.get('id'),
                'quantity': 1,
            },
        ],
        mode="payment",
        expires_at=int(time.time()) + 1830,
        success_url='https://example.com/success',

    )
    return session


def get_session(session_id: str):
    stripe.api_key = API_KEY_STRIPE

    session = stripe.checkout.Session.retrieve(session_id)
    return session
