import json

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payment.models import Order


@csrf_exempt  # disable protection against CSRF attacks, because in this case we don’t need it
def stripe_webhook(request):
    '''
    We add items to the cart and make an inquiry. During the processing of this process, there may be some kind of
    error, such as insufficient funds in the buyer's account. Webhook works through events: it listens to events and takes actions based on them.
    based on them performs certain actions.

    Where do we get an event from? From stripe.
    '''

    payload = request.body  # Get the body of the HTTP request that contains the JSON-formatted data sent by Stripe.
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']  # Retrieve the HTTP_STRIPE_SIGNATURE header that contains the request signature created by Stripe.
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

            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()

    return HttpResponse(status=200)



