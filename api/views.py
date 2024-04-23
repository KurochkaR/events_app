from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event
from .serializers import EventSerializer


class EventListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Event.objects.all()
        search_query = request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) |
                                       Q(location__icontains=search_query)).distinct()
        # location = request.query_params.get('location')
        # if location:
        #     queryset = queryset.filter(location=location)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        mutable_data = request.data.copy()
        mutable_data['organizer'] = request.user.pk
        serializer = EventSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Event, pk=pk)

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def post(self, request, pk):
        event = self.get_object(pk)
        if event.organizer != request.user:
            try:
                if request.user in event.attendees.all():
                    return Response({'message': "You are already registered for this event"},
                                    status=status.HTTP_400_BAD_REQUEST)
                event.attendees.add(request.user)
                subject = 'Event Registration Confirmation'
                message = f'You have successfully registered for the event "{event.title}".'
                recipient_list = [request.user.username]
                from_email = "Eventsapp@gmail.com"
                send_mail(subject, message, from_email, recipient_list)

                return Response({'message': 'You have successfully registered for the event'},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "Organizers cannot be attendees"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event = self.get_object(pk)
        if event.organizer != request.user:
            return Response({'error': 'You are not the organizer of this event'}, status=status.HTTP_403_FORBIDDEN)
        mutable_data = request.data.copy()
        mutable_data.pop('organizer', None)
        serializer = EventSerializer(event, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        event = self.get_object(pk)
        if event.organizer != request.user:
            return Response({'error': 'You are not the organizer of this event'}, status=status.HTTP_403_FORBIDDEN)

        mutable_data = request.data.copy()
        mutable_data.pop('organizer', None)
        serializer = EventSerializer(event, data=mutable_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)