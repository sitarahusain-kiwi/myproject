from django.db import models


# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract model that provides fields required
    for most models such as creation time, updated time.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for TimeStampedModel Model
        """
        abstract = True