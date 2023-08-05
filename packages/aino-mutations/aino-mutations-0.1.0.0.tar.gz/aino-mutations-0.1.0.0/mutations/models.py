from django.db import models


class MutationLog(models.Model):
    mutation = models.CharField(max_length=500, unique=True)

