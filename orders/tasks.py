# django import
from django.core.mail import send_mail
# celery import
from celery import task
# local import
from .models import Order


@task
def order_created(order_id):
    '''
    Task to send an e-mail notification when an order is successfully created.
    '''
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have been successfully place an order.\
                   Your order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
