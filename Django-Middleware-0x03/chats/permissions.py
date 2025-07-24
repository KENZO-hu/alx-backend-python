from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation or message
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission that allows only authenticated users who are participants of the conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users
        if not (request.user and request.user.is_authenticated):
            return False
        # Allow safe methods for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Explicitly check for PUT, PATCH, DELETE methods
        if request.method in ["PUT", "PATCH", "DELETE"]:
            conversation_id = view.kwargs.get('conversation_pk') or view.kwargs.get('conversation_id')
            if not conversation_id:
                return False
            # Additional permission checks can be done in has_object_permission
            return True
        # For other methods, deny access
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation or message
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
