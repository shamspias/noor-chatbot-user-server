from django.http import HttpResponse
import stripe
from django.conf import settings

from ausers.models import User


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

    if event['type'] == 'charge.succeeded':
        # Get the email address associated with the payment
        email = event['data']['object']['billing_details']['email']
        # Get the user from the database
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Update the payment status of the user
            user.subscription_status = True
            user.save()
        else:
            User.objects.create_user(email=email, password="123456789", subscription_status=True)

    return HttpResponse(status=200)
