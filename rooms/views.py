from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Room, Slot, Waitlist, free_slot
from .serializers import RoomSerializer, SlotSerializer, WaitlistSerializer

class RoomViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @swagger_auto_schema(tags=['Rooms'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rooms'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rooms'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rooms'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rooms'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Rooms'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class SlotViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    @swagger_auto_schema(tags=['Slot'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Slot'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Slot'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Slot'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Slot'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Slot'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Slot'])
    @action(detail=True, methods=['post'])
    def cancel_reservation(self, request, pk=None):
        slot = Slot.objects.get(pk=pk)

        if slot.reserved_user == request.user:
            free_slot(slot)
            return Response({"message": "Reservation canceled, slot is now free."})
        else:
            return Response({"message": "You do not have a reservation for this slot."}, status=403)


class WaitlistViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer

    @swagger_auto_schema(tags=['Waitlist'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Waitlist'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Reserve free slot from list!", tags=['Waitlist'])
    def create(self, request, *args, **kwargs):
        return self.reserve_slot(request)

    @swagger_auto_schema(tags=['Waitlist'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Waitlist'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Deactivated, request is not available!",tags=['Waitlist'])
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Deleting a waitlist entry is not allowed.")

    def reserve_slot(self, request):
        user = request.user
        room_id = request.data.get('room_id')
        room = Room.objects.get(id=room_id)

        available_slot = Slot.objects.filter(room=room, occupation_status=Slot.STATUS_ON_HOLD).first()

        if available_slot:
            available_slot.occupation_status = Slot.STATUS_ACTIVE
            available_slot.reserved_user = user
            available_slot.save()

            print("You was assigned to room!")

            return Response({"message": "Slot reserved successfully", "slot_id": available_slot.id})
        else:
            waitlist_entry, created = Waitlist.objects.get_or_create(user=user, room=room, is_reserved=False)

            if created:
                return Response({"message": "No available slot, added to the waitlist"})
            else:
                return Response({"message": "User is already on the waitlist"}, status=400)