from django.db import models
from django.utils.translation import ugettext_lazy as _

from pretix.base.models import Event, Item, Organizer, SubEvent


class SeatingPlan(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Name'))
    organizer = models.ForeignKey(Organizer, related_name='seating_plans', on_delete=models.CASCADE)
    layout = models.TextField()


class SeatCategoryMapping(models.Model):
    event = models.ForeignKey(Event, related_name='seat_category_mappings', on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent, related_name='seat_category_mappings', on_delete=models.CASCADE)
    layout_category = models.CharField(max_length=190)
    product = models.ForeignKey(Item, related_name='seat_category_mappings', on_delete=models.CASCADE)


class Seat(models.Model):
    event = models.ForeignKey(Event, related_name='seats', on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent, related_name='seats', on_delete=models.CASCADE)
    name = models.CharField(max_length=190)
    layout_category = models.CharField(max_length=190)
    blocked = models.BooleanField(default=False)
