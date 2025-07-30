from django.views.decorators.cache import cache_page
from .managers import UnreadMessagesManager

# ...existing code...

from .models import Message

@cache_page(60)
@login_required
def unread_inbox(request):
    # Use the classmethod to get unread messages for the user, optimized with .only()
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp').select_related('sender')
    return render(request, 'messaging/unread_inbox.html', {'unread_messages': unread_messages})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def user_conversation(request):
    messages = Message.objects.filter(sender=request.user).select_related('receiver').prefetch_related('replies')
    return render(request, 'messaging/user_conversation.html', {'messages': messages})

@login_required
def threaded_conversation(request, message_id):
    root_message = get_object_or_404(Message, id=message_id)
    def get_replies(message):
        replies = list(message.replies.select_related('sender', 'receiver').all())
        for reply in replies:
            reply.child_replies = get_replies(reply)
        return replies
    thread = {
        'root': root_message,
        'replies': get_replies(root_message)
    }
    return render(request, 'messaging/threaded_conversation.html', {'thread': thread})
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account and all related data have been deleted.")
        return redirect('home')
    messages.error(request, "Invalid request method.")
    return redirect('profile')
