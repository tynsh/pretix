import json

from pretix.base.models import Event, Seat, SubEvent


def refresh_seat_cache(event: Event, subevent: SubEvent):
    plan = subevent.seating_plan if subevent else event.seating_plan
    layout = json.loads(plan.layout)
    seat_cache = {
        seat.name: seat for seat in event.seats.filter(subevent=subevent)
    }
    seats_create = []

    for zone in layout['zones']:
        for row in zone['rows']:
            for s in row['seats']:
                sname = '{} {}'.format(row['row_number'], s['seat_number'])
                layout_category = s.get('category', 'CAT')  # TODO: Real categories

                if sname in seat_cache:
                    seat = seat_cache.pop(sname)
                    if seat.layout_category != layout_category:
                        seat.layout_category = layout_category
                        seat.save()
                else:
                    seat = Seat(
                        event=event,
                        subevent=subevent,
                        name=sname
                    )
                    seat.layout_category = layout_category
                    seat.save()

    Seat.objects.bulk_create(seats_create)
