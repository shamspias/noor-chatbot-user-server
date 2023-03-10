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
    email = obj['email']
    phone = obj['phone']
    name = obj['name']
    stripe_id = obj['id']
    return User.objects.create_user(email=email, password="123456789", phone_number=phone, first_name=name,
                                    stripe_id=stripe_id, subscription_status=True)


@csrf_exempt
def stripe_webhook(request):
    if request.method == 'GET':
        return HttpResponse(status=400)
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            print(event['type'])
        except ValueError as e:
            # Invalid payload
            print("invalid payload")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print("invalid signature")
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'checkout.session.async_payment_succeeded':
            session = event['data']['object']

        elif event['type'] == 'checkout.session.completed':
            session = event['data']['object']

        elif event['type'] == 'customer.created' or event['type'] == 'customer.updated':
            customer = event['data']['object']
            # Get the email address
            email = customer['email']
            phone = customer['phone']
            name = customer['name']
            stripe_id = customer['id']
            # Get the user from the database
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                # Update the payment status of the user
                user.phone_number = phone
                user.first_name = name
                user.stripe_id = stripe_id
                user.subscription_status = True
                user.save()
            else:
                create_user_from_stripe(customer)

        elif event['type'] == 'customer.deleted':
            customer = event['data']['object']
            email = customer['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.delete()

        elif event['type'] == 'customer.subscription.created' or event['type'] == 'customer.subscription.resumed':
            subscription = event['data']['object']
            email = subscription['email']
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
            email = subscription['email']
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
