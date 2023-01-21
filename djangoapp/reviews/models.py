from djangoapp.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    followed_user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by"
    )

    class Meta:
        unique_together = ("user", "followed_user")


class Ticket(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, blank=True)
    time_created = models.fields.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE
    )
    rating = models.fields.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    headline = models.fields.CharField(max_length=128)
    body = models.fields.TextField(max_length=8192)
    time_created = models.fields.DateTimeField(auto_now_add=True)
