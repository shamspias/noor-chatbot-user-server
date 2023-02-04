from rest_framework.routers import SimpleRouter
from django.urls import path
from ausers.views import UserViewSet

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)
#
# urlpatterns = [
#     path('status', UserStatus.as_view(), name="check-user"),
# ]
