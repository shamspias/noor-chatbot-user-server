from rest_framework.routers import SimpleRouter

from ausers.views import UserViewSet, CustomerViewSet

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)
