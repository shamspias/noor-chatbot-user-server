from rest_framework.routers import SimpleRouter

from django.urls import path
from .views import DeleteConversationalHistoryApiView, TrackConversationHistory, UpdateTrackConversationHistory

from ausers.views import UserViewSet

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)

urlpatterns = [
    path('track/', TrackConversationHistory.as_view(), name='conversation-track'),
    path('update/', UpdateTrackConversationHistory.as_view(), name='conversation-update'),
    path('delete/', DeleteConversationalHistoryApiView.as_view(), name='conversation-delete'),
]
