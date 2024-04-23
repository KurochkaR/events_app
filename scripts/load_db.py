from django.db import IntegrityError

from api.models import Event
from authorization.models import CustomUser

events_data = [
    {
        'title': "Music Festival",
        'description': "Join us for a day of live music performances from local and international artists. Food and drinks will be available.",
        'date': "2024-08-15 18:00",
        'location': "Central Park",
        'organizer_id': 3,
    },
    {
        'title': "Art Exhibition",
        'description': "Explore stunning artworks by emerging and established artists. Meet the artists and discover their inspirations.",
        'date': "2024-09-20 09:15",
        'location': "Art Gallery",
        'organizer_id': 3,

    },
    {
        'title': "Fitness Bootcamp",
        'description': "Get ready to sweat it out! Join our high-intensity bootcamp workout for a full-body fitness experience.",
        'date': "2024-07-10 11:00",
        'location': "Fitness Center",
        'organizer_id': 2,
    },
    {
        'title': "Tech Conference",
        'description': "Stay up-to-date with the latest trends in technology. Learn from industry experts and network with professionals.",
        'date': "2024-10-05 17:00",
        'location': "Convention Center",
        'organizer_id': 2,
    },
    {
        'title': "Cooking Class",
        'description': "Learn to cook delicious meals from scratch. Our experienced chefs will teach you essential cooking techniques.",
        'date': "2024-07-25 11:10",
        'location': "Culinary School",
        'organizer_id': 1,
    },
    {
        'title': "Yoga Retreat",
        'description': "Escape the hustle and bustle of city life. Reconnect with yourself through yoga, meditation, and relaxation.",
        'date': "2024-09-15 14:30",
        'location': "Retreat Center",
        'organizer_id': 1,
    }
]

user_data = [
    {
        'email': 'user1@example.com',
        'password': 'user1password',
    },
    {
        'email': 'user2@example.com',
        'password': 'user2password',
    },
    {
        'email': 'user3@example.com',
        'password': 'user3password',
    }
]


def init_models():
    for user in user_data:
        email = user['email']
        password = user['password']
        if not CustomUser.objects.filter(email=email).exists():
            CustomUser.objects.create_user(username=email, email=email, password=password)
        else:
            continue

    for event in events_data:
        Event.objects.get_or_create(title=event['title'],
                                    defaults=event)


def run():
    init_models()