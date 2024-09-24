from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, SlotViewSet, WaitlistViewSet


router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'slots', SlotViewSet)
router.register(r'waitlist', WaitlistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]