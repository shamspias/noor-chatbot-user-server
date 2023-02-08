from rest_framework import viewsets, mixins, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ausers.models import User, NoneExistNumbers, ConversationHistory
from ausers.permissions import IsUserOrReadOnly
from ausers.serializers import (
    CreateUserSerializer,
    AuserSerializer,
)


class UserViewSet(mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - User Accounts
    """

    queryset = User.objects.all()
    serializers = {'default': AuserSerializer, 'create': CreateUserSerializer}
    permissions = {'default': (IsUserOrReadOnly,), 'create': (AllowAny,)}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='info', url_name='info')
    def get_user_data(self, instance):
        try:
            return Response(AuserSerializer(self.request.user, context={'request': self.request}).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='status', url_name='status')
    def get_user_status(self, request):

        try:
            number = request.GET.get("phone")
            number = '+' + number[1:]
            if User.objects.filter(phone_number=number).exists():
                customer = User.objects.get(phone_number=number)
                none_exist_number, _created = NoneExistNumbers.objects.get_or_create(number=number)
                none_exist_number.is_user = True
                none_exist_number.text_count += 1
                none_exist_number.save()
                if customer.check_user_status():
                    return Response({'status': 'paid', 'count': none_exist_number.text_count},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'free', 'count': none_exist_number.text_count},
                                    status=status.HTTP_200_OK)
            else:
                none_exist_number, _created = NoneExistNumbers.objects.get_or_create(number=number)
                none_exist_number.text_count += 1
                none_exist_number.save()
                return Response({'status': 'not exist', 'count': none_exist_number.text_count},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong request' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteConversationalHistoryApiView(views.APIView):
    """
    API View to delete all the conversation history
    """

    def post(self, request):
        """
        Send phone number to delete all conversation
        example:
        {
            "number": "+8801784056345",
        }
        """
        phone_number = request.data.get('number')
        none_exist_number_obj = NoneExistNumbers.objects.get(number=phone_number)
        ConversationHistory.objects.filter(phone_number=none_exist_number_obj).delete()
        return Response({"message": "Deleted"}, status=status.HTTP_200_OK)


class TrackConversationHistory(views.APIView):
    """
    API view to Track the conversation history and save
    """

    def post(self, request):
        """
        Send the data to chatbot
        example:
        {
            "number": "+8801784056345",
            "user_input": "Hey there! how are you",
            "end_param":"bot:",
        }
        """
        number = request.data.get('number')
        number_obj = NoneExistNumbers.objects.get(number=number)
        user_input = request.data.get('user_input')
        end_param = request.data.get('end_param', 'bot')
        if user_input is None:
            return Response({"error": "No input values"})

        # get last 15 conversation and pass to chatbot response
        chatbot_prompt = ""
        conversations = ConversationHistory.objects.filter(phone_number=number_obj).order_by('-created_at')[:15]
        for conversation in conversations:
            if conversation.user_input is None:
                conversation.user_input = ""
            if conversation.chatbot_response is None:
                conversation.chatbot_response = ""
            chatbot_prompt += "human:" + conversation.user_input + "\n" + end_param + conversation.chatbot_response + "\n"

        chatbot_prompt += "human:" + user_input + "\n" + end_param

        # save the user input into database
        try:
            last_conversation = ConversationHistory.objects.filter(phone_number=number_obj).latest(
                'conversation_id')
            conversation_id = last_conversation.conversation_id
            conversation_id += 1
        except:
            conversation_id = 0

        if user_input:
            conversation = ConversationHistory.objects.create(phone_number=number_obj,
                                                              conversation_id=conversation_id,
                                                              user_input=user_input)
            conversation.save()
        return Response({"prompt": chatbot_prompt, "conversation_id": conversation_id}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({
            "number": "+8801784056345",
            "user_input": "Hey there! how are you",
            "end_param": "bot:",
        }, status=status.HTTP_200_OK)
