import json

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa import Webhook

from payment.models import Order
from payment.tasks import send_order_confirmation


@csrf_exempt  # disable protection against CSRF attacks, because in this case we don’t need it
def stripe_webhook(request):
    '''
    We add items to the cart and make an inquiry. During the processing of this process, there may be some kind of
    error, such as insufficient funds in the buyer's account. Webhook works through events: it listens to events and takes actions based on them.
    based on them performs certain actions.

    Where do we get an event from? From stripe.
    '''

    payload = request.body  # Get the body of the HTTP request that contains the JSON-formatted data sent by Stripe.
    sig_header = request.META[
        'HTTP_STRIPE_SIGNATURE']  # Retrieve the HTTP_STRIPE_SIGNATURE header that contains the request signature created by Stripe.
    event = None

    try:
        # signature verification and construction of the Stripe event object. If the signature does not match the
        # expected signature, an exception is thrown
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order_id = session.client_reference_id
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            send_order_confirmation.delay(order_id)
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()

    return HttpResponse(status=200)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def yookassa_webhook(request):
    webhook = Webhook(request.body, request.headers['Content-Type'])
    event = webhook.parse()

    # handle payment event
    if event.type == 'payment.succeeded':
        return HttpResponse(status=200)

    return HttpResponse(status=200)

    ip = get_client_ip(request)  # get request ip
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    # extract JSON object from request body
    event_json = json.loads(request.body)
    try:
        # creating a notification class object based on an event
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # specific logic
            # ...

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        else:
            # errors handle
            return HttpResponse(status=400)  # send info about error to YooKassa

        Configuration.configure('XXXXXX', 'test_XXXXXXXX')
        # get actual info about payment
        payment_info = Payment.find_one(some_data['paymentId'])

        if payment_info:
            try:
                order_id = payment_info['id']
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            payment_status = payment_info.status

            # specific logic
            if payment_status == 'succeeded':
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.save()
            else:
                raise ValueError('Payment status is unsuccessful. An error has occurred')
        else:
            # error handle
            return HttpResponse(status=400)  # send info about error to YooKassa

    except Exception:
        # error handle
        return HttpResponse(status=400)  # send info about error to YooKassa

    return HttpResponse(status=200)
