from django.db import models


class Programs(models.Model):
    data = models.JSONField(null=True, unique=True)