from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        self.assertTrue(Notification.objects.filter(user=self.receiver, message=msg).exists())

    def test_message_edit_logs_history(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        msg.content = 'Hello, edited!'
        msg.save()
        self.assertTrue(MessageHistory.objects.filter(message=msg, old_content='Hello!').exists())

    def test_unread_messages_manager(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        unread = Message.objects.for_user(self.receiver)
        self.assertIn(msg, unread)
        msg.read = True
        msg.save()
        unread = Message.objects.for_user(self.receiver)
        self.assertNotIn(msg, unread)
