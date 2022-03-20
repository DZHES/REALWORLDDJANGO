from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce

class EventQuerySet(models.QuerySet):
    def count_enrolls(self):
        return self.annotate(count_left=Coalesce(models.Count('enrolls'), 0))