from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

from ausers.models import User


def create_user_from_stripe(obj):
    """
    create user
    :return: user instance
    """
    email = obj['billing_details']['email']
    phone = obj['billing_details']['phone']
    name = obj['billing_details']['name']
    stripe_id = obj['billing_details']['id']
    return User.objects.create_user(email=email, password="123456789", phone_number=phone, first_name=name,
                                    stripe_id=stripe_id)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']

    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
    elif event['type'] == 'customer.created':
        customer = event['data']['object']
        # Get the email address
        email = customer['billing_details']['email']
        phone = customer['billing_details']['phone']
        name = customer['billing_details']['name']
        stripe_id = customer['billing_details']['id']
        # Get the user from the database
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Update the payment status of the user
            user.phone_number = phone
            user.first_name = name
            user.stripe_id = stripe_id
            user.save()
        else:
            create_user_from_stripe(customer)

    elif event['type'] == 'customer.deleted':
        customer = event['data']['object']
        email = customer['billing_details']['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.delete()

    elif event['type'] == 'customer.subscription.created' or event['type'] == 'customer.subscription.resumed':
        subscription = event['data']['object']
        email = subscription['billing_details']['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Update the payment status of the user
            user.subscription_status = True
            user.save()
        else:
            user = create_user_from_stripe(subscription)
            user.subscription_status = True
            user.save()

    elif event['type'] == 'customer.subscription.deleted' or event['type'] == 'customer.subscription.paused':
        subscription = event['data']['object']
        email = subscription['billing_details']['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Update the payment status of the user
            user.subscription_status = False
            user.save()
        else:
            user = create_user_from_stripe(subscription)
            user.subscription_status = False
            user.save()

    elif event['type'] == 'customer.subscription.trial_will_end':
        subscription = event['data']['object']
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)
