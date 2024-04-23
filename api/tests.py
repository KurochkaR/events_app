from datetime import datetime

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate, APITestCase
from rest_framework import status
from authorization.models import CustomUser
from .models import Event
from .views import EventListCreateAPIView


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com',
                                                   password='testpassword')

    def test_login_view(self):
        client = Client()
        response = client.post(reverse('rest_framework:login'), {'username': 'testuser@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to the home page upon successful login

    def test_invalid_login(self):
        client = Client()
        response = client.post(reverse('rest_framework:login'), {'username': 'testuser@example.com', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct email and password.')


class EventModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com',
                                                   password='testpassword')
        self.event = Event.objects.create(title='Test Event',
                                          description='Test Description',
                                          date=datetime(2024,5,5),
                                          location="Kyiv",
                                          organizer=self.user)

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.title, 'Test Event')

    def test_event_str_method(self):
        self.assertEqual(str(self.event), 'Test Event')


class EventViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com',
                                                   password='testpassword')
        self.event = Event.objects.create(title='Test Event',
                                          description='Test Description',
                                          date=datetime(2024, 5, 5),
                                          location="Kyiv",
                                          organizer=self.user)

    def test_event_list_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_detail_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('event-detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_list_view_no_auth(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 403)

    def test_event_detail_view_no_auth(self):
        response = self.client.get(reverse('event-detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 403)


class SearchTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(email='testuser@example.com',
                                                   password='testpassword')
        self.event1 = Event.objects.create(title='Event 1', description='Description 1',
                                           date=datetime(2024, 5, 5),
                                           location="Kyiv",
                                           organizer=self.user)
        self.event2 = Event.objects.create(title='Event 2', description='Description 2',
                                           date=datetime(2024, 5, 5),
                                           location="Kyiv",
                                           organizer=self.user)
        self.event3 = Event.objects.create(title='Another Event', description='Description 3',
                                           date=datetime(2024, 5, 5),
                                           location="Kyiv",
                                           organizer=self.user)

    def test_search_by_title(self):
        view = EventListCreateAPIView.as_view()
        request = self.factory.get('/events/', {'search': 'Event 1'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Event 1')

    def test_search_by_location(self):
        view = EventListCreateAPIView.as_view()
        request = self.factory.get('/events/', {'search': 'Kyiv'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['location'], 'Kyiv')

    def test_search_no_results(self):
        view = EventListCreateAPIView.as_view()
        request = self.factory.get('/events/', {'search': 'NonExistent'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


class EventAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com',
                                                   password='testpassword')
        self.user2 = CustomUser.objects.create_user(email='testuser2@example.com',
                                                   password='testpassword')
        self.event = Event.objects.create(title='Event 1', description='Description 1',
                                           date=datetime(2024, 5, 5),
                                           location="Kyiv",
                                           organizer=self.user)
        self.another_event = Event.objects.create(title='Event 2', description='Description 2',
                                          date=datetime(2024, 5, 5),
                                          location="Kyiv",
                                          organizer=self.user2)
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_list_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event(self):
        url = reverse('event-list')
        data = {'title': 'New Event',
                'description': 'New description',
                'location': 'Lviv',
                'date': datetime(2024, 5, 5)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_event = Event.objects.get(title='New Event')
        self.assertEqual(created_event.organizer, self.user)

    def test_retrieve_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_attendees(self):
        url = reverse('event-detail', kwargs={'pk': self.another_event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.another_event.refresh_from_db()
        self.assertIn(self.user, self.another_event.attendees.all())

    def test_add_organizer_as_attendees(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_update_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        data = {'title': 'Update Event',
                'description': 'Update description',
                'location': 'Lviv updated',
                'date': datetime(2024, 5, 5)}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_another_event(self):
        url = reverse('event-detail', kwargs={'pk': self.another_event.pk})
        data = {'title': 'Update Event',
                'description': 'Update description',
                'location': 'Lviv updated',
                'date': datetime(2024, 5, 5)}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        data = {'title': 'Partial Update'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)