import re
from datetime import datetime, date
from typing import Union

from .errors import InvalidAPIUsage


def validate_phone_number(phone_number: str):
    if not phone_number.isdigit():
        raise ValueError
    return phone_number


def validate_list_of_order_lines(order_lines: list, *args, created_date=None) -> list:
    created_date = created_date if created_date else date.today()
    if order_lines:
        for service in order_lines:

            quantity, service_id, event_date = (service.get('quantity'),
                                                service.get('service_id'),
                                                service.get('event_date') or '')

            if not (type(quantity) == int and quantity > 0):
                raise ValueError('Order lines must have quantity and it should be a positive number.')

            if not (type(service_id) == int and service_id > 0):
                raise ValueError('Service_id in order_lines must be positive number.')

            date_regex = r'^\d{4}-\d{2}-\d{1,2}$'
            if not bool(re.match(date_regex, event_date)):
                raise ValueError('Date must be in format: "2023-01-01"')
            if datetime.strptime(event_date, '%Y-%m-%d').date() < created_date:
                raise ValueError('Event date must be equal or greater than created_date')

        return order_lines

    raise ValueError('order_lines must be a list of dicts that consist of service_id, quantity and event_date.')


def validate_page_and_per_page(
        page: Union[int, str],
        per_page: Union[int, str]
) -> tuple[int, int] | Exception:
    try:
        valid_page = int(page)
        valid_per_page = int(per_page)
    except ValueError:
        raise InvalidAPIUsage('Page and per_page must be numbers')
    else:
        return valid_page, valid_per_page


def validate_dates(date_from: str, date_by: str) -> tuple[date, ...]:
    if date_from is None and date_by is None:
        raise InvalidAPIUsage('Two dates must be indicated and first date must be less than second date')
    try:
        if None in (date_from, date_by):
            date = datetime.strptime(*[date for date in (date_from, date_by) if date is not None], '%Y-%m-%d')
            return date,
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_by = datetime.strptime(date_by, '%Y-%m-%d')
        if date_from > date_by:
            raise InvalidAPIUsage('First date must be less than second date')
        return date_from, date_by
    except ValueError:
        raise InvalidAPIUsage('Date must be in format: "2023-01-01"')


def validate_prices(price_from: str, price_by: str) -> tuple[int, ...]:
    prices = tuple(filter(
        lambda price: price is not None and price.isdigit(),
        (price_from, price_by)
    ))
    if not prices:
        raise InvalidAPIUsage('Prices must be positive numbers and at least one price must be indicated.')
    prices = tuple(map(int, prices))
    if len(prices) == 1 or (len(prices) == 2 and prices[0] < prices[1]):
        return prices
    raise InvalidAPIUsage('First price must be less than second price.')




