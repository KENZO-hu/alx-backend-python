
#!/usr/bin/env python3
"""Viewsets for chats"""

from rest_framework import viewsets, filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipant, IsParticipantOfConversation

from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        # Return conversations where the authenticated user is a participant
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def check_permissions(self, request):
        super().check_permissions(request)
        # Check if conversation_id is in the request for unsafe methods
        if request.method not in ['GET', 'HEAD', 'OPTIONS']:
            conversation_id = self.kwargs.get('pk') or self.kwargs.get('conversation_id')
            if conversation_id:
                if not Conversation.objects.filter(id=conversation_id, participants=request.user).exists():
                    raise PermissionDenied(detail="You do not have permission to modify this conversation.", code=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def status(self, request):
        count = self.get_queryset().count()
        return Response({'status': 'ConversationViewSet is active', 'count': count})


from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import MessagePagination

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Return messages in conversations where the authenticated user is a participant
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def check_permissions(self, request):
        super().check_permissions(request)
        # Check if conversation_id is in the request for unsafe methods
        if request.method not in ['GET', 'HEAD', 'OPTIONS']:
            conversation_id = request.data.get('conversation_id') or self.kwargs.get('conversation_id')
            if conversation_id:
                if not Conversation.objects.filter(id=conversation_id, participants=request.user).exists():
                    raise PermissionDenied(detail="You do not have permission to modify messages in this conversation.", code=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def status(self, request):
        count = self.get_queryset().count()
        return Response({'status': 'MessageViewSet is active', 'count': count})
