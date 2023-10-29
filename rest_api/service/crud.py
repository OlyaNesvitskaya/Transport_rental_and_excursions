"""Execute database queries"""
from typing import Union, Type
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from rest_api.models.models import Client, Service, Order, Order_line, db
from rest_api.rest.errors import InvalidAPIUsage


def get_all_records(cls: Type[Union[Client, Service]]) -> list:
    """Get list of records.

    Keyword argument:
    cls -- name of model for database table.
    """
    result = db.session.query(cls).all()
    return result


def get_record(cls: Type[Union[Client, Service]], record_id: int) -> Type[Union[Client, Service]]:
    """Get one record.

    Keyword arguments:
    cls -- name of model for database table;
    record_id -- id for searched record.
    """
    result = db.first_or_404(db.select(cls).filter_by(id=record_id),
                             description='Record with id={} is not available'.format(record_id))

    return result


def create_new_record(cls: Type[Union[Client, Service]], param: dict) -> Union[dict, Exception]:
    """Create a record in specified database table with specified data.

    Keyword arguments:
    cls -- name of model for database table;
    param -- the values to be inserted in database table.
    """
    try:
        new_record = cls(**param)
        db.session.add(new_record)
        db.session.commit()
        return {'code': 200, 'message': f'New {cls.__name__.lower()} with id={new_record.id} created successfully', 'record_id':new_record.id}

    except IntegrityError as e:
        db.session.rollback()
        error = 'This phone number already exists' if cls == Client else 'This service name already exists'
        raise InvalidAPIUsage(error, 409)
    except SQLAlchemyError as e:
        raise InvalidAPIUsage(e.args)


def change_record(cls: Type[Union[Client, Service]], record_id: int, args: dict) -> dict:
    """Change a record in specified database table with specified data.

    Keyword arguments:
    cls -- name of model for database table;
    record_id -- id for searched record;
    args -- the values to be inserted in database table.
    """
    try:
        value_to_change = {k: v for k, v in args.items() if v is not None}
        if value_to_change:
            db.session.execute(db.update(cls).filter_by(id=record_id).values(**value_to_change))
            db.session.commit()
        return {'message': f'Record with id={record_id} changed successfully'}
    except IntegrityError as e:
        db.session.rollback()
        error = 'This phone number already exists' if cls == Client else 'This service name already exists'
        raise InvalidAPIUsage(error, 409)


def delete_record(cls: Type[Union[Client, Service, Order]], record_id: int) -> None:
    """Delete a record in specified database table with specified data.

    Keyword arguments:
    cls -- name of model for database table;
    record_id -- id for searched record.
    """
    try:
        record_to_delete = get_record(cls, record_id)
        db.session.delete(record_to_delete)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        error = f"This {str(cls.__name__).lower()} cannot be deleted, because of presenting in orders"
        raise InvalidAPIUsage(error, 409)


def create_new_order(args: dict) -> dict:
    """Create new order with specified data.

    Keyword arguments:
    args -- the values to be inserted in database table.
    """
    try:
        new_record = Order(client_id=args['client_id'])
        db.session.add(new_record)
        db.session.commit()
        for row in args['services']:
            order_line = Order_line(order_id=new_record.id,
                                    service_id=row.get('service_id'),
                                    quantity=row.get('quantity'),
                                    event_date=row.get('event_date')
                                    )
            db.session.add(order_line)
            db.session.commit()
        return {'message': f'New order with id={new_record.id} created successfully', 'record_id': new_record.id}

    except IntegrityError as e:
        db.session.rollback()
        error = "This client_id hasn\'t existed yet"
        raise InvalidAPIUsage(error, 409)


def change_order_record(order_id: int, args: dict) -> dict:
    """Change the existing order with specified data.

    Keyword arguments:
    args -- the values to be inserted in database table instead of existing one.
    """
    try:
        if args:
            if args.get('client_id'):
                db.session.execute(db.update(Order).filter_by(id=order_id).values(client_id=args.get('client_id')))
            if args['services'] is not None:
                records_to_delete = db.session.query(Order_line).filter_by(order_id=order_id).all()
                [db.session.delete(record) for record in records_to_delete]
                for row in args['services']:
                    order_line = Order_line(order_id=order_id,
                                            service_id=row.get('service_id'),
                                            quantity=row.get('quantity'),
                                            event_date=row.get('event_date')
                                            )
                    db.session.add(order_line)
            db.session.commit()
            return {'message': f'Record {order_id} changed successfully'}
        return {'message': f'New data for {order_id} didnt be indicate'}
    except IntegrityError:
        db.session.rollback()
        error = "This client_id hasn\'t existed yet"
        raise InvalidAPIUsage(error, 409)


def filter_by_two_dates(cls: Type[Union[Client, Order]], date_1: str, date_2: str) -> list:
    """Select data about specified period.

    Keyword arguments:
    cls -- name of model in accordance with database table;
    date_1 -- start date of period;
    date_2 -- finish date of period.
    """
    result = db.session.query(cls).filter(cls.created_date.between(date_1, date_2)).all()
    return result


def filter_by_date(cls: Type[Union[Client, Order]], date):
    """Select data about specified date.

    Keyword arguments:
    cls -- name of model in accordance with database table;
    date -- date to select data.
    """
    result = db.session.query(cls).filter(cls.created_date == date[0]).all()
    return result


def filter_by_price(cls: Type[Union[Service]], price_1: str, price_2: str):
    """select data on specified prices.

    Keyword arguments:
    cls -- name of model in accordance with database table;
    price_1 -- start price;
    price_2 -- finish price.
    """
    if price_1 and price_2:
        result = db.session.query(cls).filter(cls.price.between(price_1, price_2)).all()
    else:
        price = price_1 or price_2
        result = db.session.query(cls).filter(cls.price == price).all()
    return result