from datetime import datetime, date
from rest_api.rest.errors import InvalidAPIUsage


def validation_phone_number(phone_number):
    if not phone_number.isdigit():
        raise ValueError
    return phone_number


def validate_dates(date_1, date_2):
    if date_1 is None and date_2 is None:
        raise InvalidAPIUsage('Two dates must be indicated and first date must be less than second date')
    try:
        if None in (date_1, date_2):
            date = datetime.strptime(*[date for date in (date_1, date_2) if date is not None], '%Y-%m-%d')
            return date,
        date_1 = datetime.strptime(date_1, '%Y-%m-%d')
        date_2 = datetime.strptime(date_2, '%Y-%m-%d')
        if date_1 > date_2:
            raise InvalidAPIUsage('First date must be less than second date')
        return date_1, date_2
    except ValueError:
        raise InvalidAPIUsage('Date must be in format: "2023-01-01"')


def validate_prices(price_1, price_2):
    if price_1 is None and price_2 is None:
        raise InvalidAPIUsage('Two prices must be indicated and first price must be less than second price')
    if price_1 and price_2 and int(price_1) > int(price_2):
        raise InvalidAPIUsage('First price must be less than second price')
    return price_1, price_2


def validate_list_of_services(services, created_date=None):
    created_date = created_date if created_date else date.today()
    if services:
        if all((set(service.keys()) >= {'service_id', 'quantity', 'event_date'} and
                datetime.strptime(service.get('event_date'), '%Y-%m-%d').date() >= created_date
                for service in services)):
            return services
    raise ValueError

