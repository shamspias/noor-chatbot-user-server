from rest_framework import viewsets, mixins, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ausers.models import User
from ausers.permissions import IsUserOrReadOnly
from ausers.serializers import (
    CreateUserSerializer,
    UserSerializer,
)


class UserViewSet(mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - User Accounts
    """

    queryset = User.objects.all()
    serializers = {'default': UserSerializer, 'create': CreateUserSerializer}
    permissions = {'default': (IsUserOrReadOnly,), 'create': (AllowAny,)}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='info', url_name='info')
    def get_user_data(self, instance):
        try:
            return Response(UserSerializer(self.request.user, context={'request': self.request}).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserStatus(views.APIView):
    """
    API View to check the user exists or is a paid user or not
    """

    def post(self, request, *args, **kwargs):
        """
        :param request: phone_number
        :return: string
        """
        number = request.data.get('phone_number')
        if User.objects.get(phone_number=number).exists():
            customer = User.objects.get(phone_number=number)
            if customer.check_user_status():
                return Response({'status': 'paid'})
            else:
                return Response({'status': 'free'})
        else:
            return Response({'status': 'not exist'})
