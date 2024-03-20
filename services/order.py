from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None,
) -> Order:
    with transaction.atomic():
        if tickets and username:
            user = User.objects.get(username=username)
            order = Order.objects.create(user=user)
            if date:
                order.created_at = date
                order.save()
            for ticket_data in tickets:
                ticket = Ticket.objects.create(
                    movie_session_id=ticket_data["movie_session"],
                    row=ticket_data["row"],
                    seat=ticket_data["seat"],
                    order=order,
                )
                ticket.save()
            return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(
            user__username=username
        ).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")