import json
from collections import namedtuple

import jsonschema
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from pretix.base.models import Event, Item, LoggedModel, Organizer, SubEvent


@deconstructible
class SeatingPlanLayoutValidator:
    def __call__(self, value):
        try:
            val = json.loads(value)
        except ValueError:
            raise ValidationError(_('Your layout file is not a valid JSON file.'))
        with open(finders.find('seating/seating-plan.schema.json'), 'r') as f:
            schema = json.loads(f.read())
        try:
            jsonschema.validate(val, schema)
        except jsonschema.ValidationError as e:
            raise ValidationError(_('Your layout file is not a valid seating plan. Error message: {}').format(str(e)))


class SeatingPlan(LoggedModel):
    name = models.CharField(max_length=190, verbose_name=_('Name'))
    organizer = models.ForeignKey(Organizer, related_name='seating_plans', on_delete=models.CASCADE)
    layout = models.TextField(validators=[SeatingPlanLayoutValidator()])

    Category = namedtuple('Categrory', 'name')
    RawSeat = namedtuple('Seat', 'name number row category')

    def __str__(self):
        return self.name

    @property
    def layout_data(self):
        return json.loads(self.layout)

    @layout_data.setter
    def layout_data(self, v):
        self.layout = json.dumps(v)

    def get_categories(self):
        return [
            self.Category(name=c['name'])
            for c in self.layout_data['categories']
        ]

    def iter_all_seats(self):
        for z in self.layout_data['zones']:
            for r in z['rows']:
                for s in r['seats']:
                    yield self.RawSeat(
                        number=s['seat_number'],
                        name='{} {}'.format(r['row_number'], s['seat_number']),  # TODO: Zone? Variable scheme?
                        row=r['row_number'],
                        category=s['category']
                    )


class SeatCategoryMapping(models.Model):
    event = models.ForeignKey(Event, related_name='seat_category_mappings', on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent, null=True, blank=True, related_name='seat_category_mappings', on_delete=models.CASCADE)
    layout_category = models.CharField(max_length=190)
    product = models.ForeignKey(Item, related_name='seat_category_mappings', on_delete=models.CASCADE)


class Seat(models.Model):
    event = models.ForeignKey(Event, related_name='seats', on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent, null=True, blank=True, related_name='seats', on_delete=models.CASCADE)
    name = models.CharField(max_length=190)
    product = models.ForeignKey('Item', null=True, blank=True, related_name='seats', on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
