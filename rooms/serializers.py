from rest_framework import serializers
from .models import Room, Slot, Waitlist

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'max_time', 'max_users']


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'occupation_time', 'user_count', 'occupation_status',
                  'room', 'reserved_user']


class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ['id', 'user', 'room', 'slot', 'joined_time', 'is_reserved']