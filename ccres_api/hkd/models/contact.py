from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class AlertContactGroup(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        verbose_name = "Group of contact for alerting"

    def __str__(self):
        return f"{self.name}"


class AlertContact(models.Model):
    name = models.TextField()
    email = models.TextField()
    groups = models.ManyToManyField(AlertContactGroup)

    class Meta:
        verbose_name = "Contact for alerting"
        unique_together = ("name", "email")

    def __str__(self):
        return f"{self.name}"
