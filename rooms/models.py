import uuid

from django.db import models
from django.utils import timezone
from datetime import timedelta

from users.models import User


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=True, default='Main Office')
    max_time = models.IntegerField(default=30)
    max_users = models.IntegerField(default=1)

    class Meta:
        ordering = ['title']


def free_slot(slot):
    slot.occupation_status = Slot.STATUS_ON_HOLD
    slot.reserved_user = None
    slot.save()

    next_waitlist_entry = Waitlist.objects.filter(room=slot.room, is_reserved=False).order_by('joined_time').first()

    if next_waitlist_entry:
        slot.occupation_status = Slot.STATUS_ACTIVE
        slot.reserved_user = next_waitlist_entry.user
        slot.save()

        next_waitlist_entry.is_reserved = True
        print("You was assigned to room from waitlist, please confirm your reservation!")
        next_waitlist_entry.save()

        return next_waitlist_entry.user
    return None


class Slot(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_ON_HOLD = 'on_hold'
    STATUS_UNABLED = 'unabled'

    OCCUPATION_STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_ON_HOLD, 'On Hold'),
        (STATUS_UNABLED, 'Unabled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    occupation_time = models.IntegerField(default=30)
    user_count = models.IntegerField(default=1)
    occupation_status = models.CharField(
        max_length=10,
        choices=OCCUPATION_STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    reserved_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['room_id']

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=30)

        if self.end_time and self.end_time <= timezone.now() and self.occupation_status == Slot.STATUS_ACTIVE:
            free_slot(self)

        super().save(*args, **kwargs)


class Waitlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, null=True, blank=True, on_delete=models.SET_NULL)
    joined_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        ordering = ['joined_time']