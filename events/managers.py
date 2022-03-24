from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce

class EventQuerySet(models.QuerySet):
    def count_enrolls(self):
        return self.annotate(count_left=Coalesce(models.Count('enrolls'), 0))

    def qs1(self):
        return self.select_related('category').prefetch_related('features', 'enrolls').count_enrolls().all()

    def qs2(self):
        return self.select_related('category').prefetch_related('reviews__user', 'features', 'enrolls__user')
