from django.utils import timezone
from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['attendees']
        extra_kwargs = {
            'description': {'required': False},
            'organizer': {'required':False}
        }

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value
