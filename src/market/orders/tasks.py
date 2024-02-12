from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order.id}'
    message = f'{order.full_name}, Вы успешно разместили заказ.Ваш заказ № {order.id}.'
    mail_sent = send_mail(subject, message, 'sales@megano.com', [order.email])
    return mail_sent
