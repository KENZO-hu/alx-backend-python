from django.db import models
from django.contrib.auth.models import User

class MessageHistory(models.Model):
    message = models.ForeignKey('messaging.Message', on_delete=models.CASCADE, related_name='edit_history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID: {self.message.id} at {self.edited_at}"
