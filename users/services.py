import stripe
import config.settings as settings
from users.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    """Создаем продукт в Stripe"""
    product = stripe.Product.create(
        name=course.title,
        description=course.content[:500]
    )
    return product.id


def create_stripe_price(course):
    """Создаем цену в Stripe"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(course.price * 100),
        product=course.stripe_product_id,
    )
    return price.id


def create_checkout_session(course, user):
    """Создает сессию оплаты"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': course.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
        metadata={
            'course_id': course.id,
            'user_id': user.id
        }
    )

    Payment.objects.create(user=user, paid_course=course, amount=course.price, payment_method='transfer')

    return session.url
