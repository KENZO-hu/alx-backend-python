from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message

@cache_page(60)
@login_required
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(parent_message_id=conversation_id).select_related('sender', 'receiver').prefetch_related('replies')
    return render(request, 'chats/conversation.html', {'messages': messages})
