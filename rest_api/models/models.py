import os
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, event, select, func
from sqlalchemy.orm import relationship, column_property
from datetime import date
from rest_api.models.database import db, load_initial_data


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    created_date = db.Column(db.Date, nullable=False, default=date.today)
    orders = relationship('Order', lazy='joined')

    def __repr__(self):
        return f'<Client {self.name}>'


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text(1000), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    orders = relationship('Order_line', lazy='joined')

    @hybrid_property
    def number_of_orders(self):
        return sum(order.quantity for order in self.orders)

    def __repr__(self):
        return f'<Service {self.name}>'


class Order_line(db.Model):
    __tablename__ = "order_line"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey("orders.id"), nullable=False)
    service_id = db.Column(db.Integer, ForeignKey("services.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    event_date = db.Column(db.Date, nullable=False, default=date.today)
    order_line_price = column_property(select(quantity * Service.price)
                                       .where(Service.id == service_id)
                                       .correlate_except(Service)
                                       .scalar_subquery(),
                                        deferred=True
                                       )


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.Date, nullable=False, default=date.today)
    client_id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    order_lines = relationship('Order_line', backref="order", cascade="all, delete-orphan")
    client = relationship('Client', viewonly=True)
    total_order_price = column_property(select(func.sum(Order_line.order_line_price))
                                        .where(Order_line.order_id == id)
                                        .correlate_except(Order_line)
                                        .scalar_subquery(),
                                        deferred=True
                                       )

    def __repr__(self):
        return f'<Order №{self.id}, client_id={self.client_id}>'


base_dir = os.path.dirname(__file__)


@event.listens_for(Client.__table__, 'after_create')
def create_clients(*args, **kwargs):
    if kwargs.get('_ddl_runner').connection.engine.url.database == 'test_db':
        pass
    else:
        load_initial_data(Client, os.path.join(base_dir, "initial_data/clients.csv"))


@event.listens_for(Service.__table__, 'after_create')
def create_service(*args, **kwargs):
    if kwargs.get('_ddl_runner').connection.engine.url.database == 'test_db':
        pass
    else:
        load_initial_data(Service, os.path.join(base_dir, "initial_data/services.csv"))


@event.listens_for(Order.__table__, 'after_create')
def create_order(*args, **kwargs):
    if kwargs.get('_ddl_runner').connection.engine.url.database == 'test_db':
        pass
    else:
        load_initial_data(Order, os.path.join(base_dir, "initial_data/order.csv"))


@event.listens_for(Order_line.__table__, 'after_create')
def create_order_line(*args, **kwargs):
    if kwargs.get('_ddl_runner').connection.engine.url.database == 'test_db':
        pass
    else:
        load_initial_data(Order_line, os.path.join(base_dir, "initial_data/order_line.csv"))

