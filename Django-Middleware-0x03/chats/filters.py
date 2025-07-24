import django_filters
from .models import Message
from django_filters import rest_framework as filters

class MessageFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    participant = filters.CharFilter(field_name="conversation__participants__username", lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['start_date', 'end_date', 'participant']
