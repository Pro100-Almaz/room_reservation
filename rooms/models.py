# from django.db import models
#
# from quickstart
#
#
#
# class Room(models.Model):
#     slots = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100, blank=True, default='')
#     code = models.TextField()
#     linenos = models.BooleanField(default=False)
#     language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
#     style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
#
#     class Meta:
#         ordering = ['created']
#
# class Slot(models.Model):
#     start_time =
#     end_time =
#     occupation_time =
#     user_count =
#     occupation_status = models.BooleanField(default=False)
#     room_id = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
#     reserved_user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
#
#     class Meta:
#         ordering = ['created']