from django.db import models
from authorization.models import CustomUser


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="organizers")
    attendees = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.title
