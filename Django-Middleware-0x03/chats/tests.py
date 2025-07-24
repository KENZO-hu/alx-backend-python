import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import User, Conversation, Message

@pytest.mark.django_db
def test_conversation_and_message_flow():
    client = APIClient()

    # Create users
    user1 = User.objects.create_user(username='user1', password='pass123')
    user2 = User.objects.create_user(username='user2', password='pass123')

    # Authenticate as user1
    client.force_authenticate(user=user1)

    # Create a conversation with user2
    url = reverse('conversation-list')
    response = client.post(url, {'participants': [user1.id, user2.id]}, format='json')
    assert response.status_code == 201
    conversation_id = response.data['id']

    # Send a message in the conversation
    url = reverse('message-list')
    response = client.post(url, {'conversation': conversation_id, 'content': 'Hello!'}, format='json')
    assert response.status_code == 201
    message_id = response.data['id']

    # Fetch conversations for user1
    url = reverse('conversation-list')
    response = client.get(url)
    assert response.status_code == 200
    assert any(conv['id'] == conversation_id for conv in response.data)

    # Fetch messages for user1 with pagination and filtering
    url = reverse('message-list') + f'?page=1&participant={user2.username}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'results' in response.data

    # Test unauthorized access
    client.force_authenticate(user=None)
    response = client.get(reverse('conversation-list'))
    assert response.status_code == 401

@pytest.mark.django_db
def test_jwt_authentication(client):
    # This test assumes JWT token endpoints are configured
    user = User.objects.create_user(username='jwtuser', password='jwtpass')
    url = reverse('token_obtain_pair')
    response = client.post(url, {'username': 'jwtuser', 'password': 'jwtpass'}, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
