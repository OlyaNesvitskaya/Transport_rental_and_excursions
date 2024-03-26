import pytest
from datetime import date, timedelta
from sqlalchemy.sql import text
from rest_api.models.models import Client, Service, Order, Order_line
from rest_api.api import db, create_app
import rest_api.config as config


def get_current_date():
    return date.today().strftime('%Y-%m-%d')


def get_date_that_was_two_days_ago():
    return (date.today() - timedelta(2)).strftime('%Y-%m-%d')


def fill_database():
    first_client = Client(created_date=get_date_that_was_two_days_ago(),
                          name='Valentina Ivanova',
                          phone_number='0997777777',
                          email='ValIv@gmail.com')

    first_service = Service(name='New_service №1',
                            description='Description №1',
                            unit='person',
                            price=50)

    first_order = Order(created_date=get_date_that_was_two_days_ago(),
                        client_id=1)

    first_order_line = Order_line(order_id=1,
                                  service_id=1,
                                  quantity=5,
                                  event_date=get_date_that_was_two_days_ago())

    db.session.add_all((first_client, first_service, first_order, first_order_line))
    db.session.commit()


@pytest.fixture()
def app():
    app = create_app(config_class=config.TestConfig)
    app.app_context().push()
    db.drop_all()
    db.create_all()
    fill_database()

    yield app

    db.session.remove()


@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()


def new_client():
    return {'model': Client, 'path': '/clients', 'payload': {
        "name": "Svitlana Kovalova",
        "phone_number": "050111111",
        "email": "Svetlana_koval@gmail.com"
    }}


def new_service():
    return {'model': Service, 'path': '/services', 'payload': {
        "name": "New_service №2",
        "description": "Description №2",
        "unit": "hour",
        "price": 100
    }}


def new_order():
    return {'model': Order, 'path': '/orders', 'payload':
            {
             "client_id": 1,
             "order_lines": [
                 {
                     "service_id": 1,
                     "quantity": 1,
                     "event_date": get_current_date()
                 }
             ]}}


def test_incorrect_resource(client):
    response = client.get('client')
    assert response.status_code == 400
    assert response.json == {"message": 'Not found'}


@pytest.mark.parametrize('new_item', [new_client(), new_service(), new_order()])
def test_create_item(app, client, new_item):
    create_item_response = client.post(f'/api{new_item["path"]}', json=new_item['payload'])

    assert create_item_response.status_code == 201

    with app.app_context():
        table_record_quantity = db.session.execute(db.select(db.func.count(new_item['model'].id))).scalar()
        assert table_record_quantity == 2

        exist_item = db.session.get(new_item['model'], 2)

        for i in new_item['payload'].keys():
            if i == 'created_date':
                formatted_event_date = exist_item.__getattribute__(i).strftime("%Y-%m-%d")
                assert formatted_event_date == new_item['payload'][i]
            elif i != 'order_lines':
                assert exist_item.__getattribute__(i) == new_item['payload'][i]
            else:
                query = db.select(Order_line).where(Order_line.order_id == 2)
                order_line = db.session.execute(query).scalars().all()
                for ind in range(len(new_item['payload']['order_lines'])):
                    for key in new_item['payload']['order_lines'][ind].keys():
                        if key == 'event_date':
                            formatted_event_date = order_line[ind].__getattribute__(key).strftime("%Y-%m-%d")
                            assert formatted_event_date == new_item['payload']['order_lines'][ind][key]
                        else:
                            assert order_line[ind].__getattribute__(key) == new_item['payload']['order_lines'][ind][key]


def test_update_client(app, client):
    update_client_response = client.put('/api/client/1', json={"name": "Row Mulrenan"})
    assert update_client_response.status_code == 201

    with app.app_context():
        assert db.session.get(Client, 1).name == "Row Mulrenan"


def test_update_service(app, client):
    update_service_response = client.put('/api/service/1', json={"name": "Skydiving"})
    assert update_service_response.status_code == 201

    with app.app_context():
        assert db.session.get(Service, 1).name == "Skydiving"


def test_update_order(app, client):
    payload = {"client_id": 1, "order_lines": [{"service_id": 1, "quantity": 20, "event_date": get_current_date()}]}
    update_order_response = client.put('/api/order/1', json=payload)
    assert update_order_response.status_code == 201

    with app.app_context():
        assert db.session.get(Order_line, 2).quantity == 20


def test_delete_order(app, client):
    delete_client_response = client.delete('/api/order/1')
    assert delete_client_response.status_code == 204


def test_delete_service(app, client):
    with app.app_context():
        db.session.execute(text('Delete from order_line where service_id = 1'))
        db.session.commit()
    delete_client_response = client.delete('/api/service/1')
    assert delete_client_response.status_code == 204


def test_delete_client(app, client):
    with app.app_context():
        db.session.execute(text('Delete from order_line where service_id = 1'))
        db.session.execute(text('Delete from orders where client_id = 1'))
        db.session.commit()
    delete_client_response = client.delete('/api/client/1')
    assert delete_client_response.status_code == 204


def test_create_client_with_not_unique_phone_number(client):
    payload = {
        "name": "Petr Petrov",
        "phone_number": "0997777777",
        "email": "petrov@gmail.com"
    }
    create_item_response = client.post(f'/api/clients', json=payload)
    assert create_item_response.status_code == 409


def test_create_service_with_not_unique_name(client):
    payload = {
        "name": "New_service №1",
        "description": "Description №2",
        "unit": "hour",
        "price": 100
    }
    create_item_response = client.post(f'/api/services', json=payload)
    assert create_item_response.status_code == 409


def test_create_order_with_absent_client(client):
    payload = {"client_id": 2, 'order_lines': [{
                    "service_id": 1,
                    "quantity": 1,
                    "event_date": get_current_date()
                }]}
    create_item_response = client.post(f'/api/orders', json=payload)
    assert create_item_response.status_code == 409


@pytest.mark.parametrize('query_string, number_of_clients, status_code',
                         [(f'?date_from={get_date_that_was_two_days_ago()}&date_by={get_current_date()}', 2, 200),
                          (f'?date_from={get_date_that_was_two_days_ago()}', 1, 200),
                          (f'?date_by={get_current_date()}', 1, 200),
                          (f'?date_by=2023-06-25', 0, 200),
                          ('', 0, 400),
                          ('?date_from=2023-06-08&date_by=2023-06-01', 0, 400),
                          ('?date_from=08-06-2023', 0, 400)
                    ])
def test_filtering_by_clients_created_dates(query_string, number_of_clients, status_code, client):
    create_client_response = client.post(f'/api/clients', json=new_client()['payload'])
    response = client.get(f'/api/clients_filtering{query_string}')
    response_body = response.json
    assert response.status_code == status_code
    if 'message' not in response_body:
        assert len(response_body.get('items', 0)) == number_of_clients


@pytest.mark.parametrize('query_string, number_of_services, status_code',
                         [('?price_from=50&price_by=110', 2, 200),
                          ('?price_from=100', 1, 200),
                          ('?price_by=50', 1, 200),
                          ('?price_by=30', 0, 200),
                          ('', 0, 400),
                          ('?price_from=100&price_by=50', 0, 400)])
def test_filtering_by_services_prices(query_string, number_of_services, status_code, client):
    create_service_response = client.post(f'/api/services', json=new_service()['payload'])
    response = client.get(f'/api/services_filtering{query_string}')
    response_body = response.json
    assert response.status_code == status_code
    if 'message' not in response_body:
        assert len(response_body.get('items', 0)) == number_of_services


@pytest.mark.parametrize('query_string, number_of_orders, status_code',
                         [(f'?date_from={get_date_that_was_two_days_ago()}&date_by={get_current_date()}', 2, 200),
                          (f'?date_from={get_date_that_was_two_days_ago()}', 1, 200),
                          (f'?date_by={get_current_date()}', 1, 200),
                          (f'?date_by=2023-06-25', 0, 200),
                          ('', 0, 400),
                          ('?date_from=2023-06-08&date_by=2023-06-01', 0, 400),
                          ('?date_from=08-06-2023', 0, 400)
                    ])
def test_filtering_by_orders_created_dates(query_string, number_of_orders, status_code, client):
    create_order_response = client.post(f'/api/orders', json=new_order()['payload'])
    response = client.get(f'/api/orders_filtering{query_string}')
    response_body = response.json
    assert response.status_code == status_code
    if 'message' not in response_body:
        assert len(response_body.get('items', 0)) == number_of_orders


@pytest.mark.parametrize('payload',
                         [
                          {"phone_number": "050111111", "email": "Svetlana_koval@gmail.com"},
                          {"name": "Svitlana Kovalova", "email": "Svetlana_koval@gmail.com"},
                          {"name": "Svitlana Kovalova", "phone_number": "050111111"}
                         ])
def test_create_client_with_mistake(client, payload):
    create_client_response = client.post('/api/clients', json=payload)
    assert create_client_response.status_code == 400


@pytest.mark.parametrize('payload',
                         [
                            {"description": "Description №2", "unit": "hour", "price": 100},
                            {"name": "New_service №2", "unit": "hour", "price": 100},
                            {"name": "New_service №2", "description": "Description №2", "price": 100},
                            {"name": "New_service №2", "description": "Description №2", "unit": "hour"}
                         ])
def test_create_service_with_mistake(client, payload):
    create_item_response = client.post('/api/services', json=payload)
    assert create_item_response.status_code == 400


@pytest.mark.parametrize('payload',
                         [
                            {"order_lines": [{"service_id": 1, "quantity": 1, "event_date": "2023-06-28"}]},
                            {"client_id": 1},
                            {"client_id": 1, "order_lines": []},
                            {"client_id": 1, "order_lines": [{"service_id": 1, "quantity": 1, "event_date": "2023-06-27"}]}
                         ])
def test_create_order_with_mistake(client, payload):
    create_order_response = client.post('/api/orders', json=payload)
    assert create_order_response.status_code == 400


def test_trying_delete_client_with_incorrect_client_id(client):
    response = client.delete('/api/client/5')
    assert response.status_code == 404


def test_trying_delete_client_with_orders(client):
    response = client.delete('/api/client/1')
    assert response.status_code == 409


def test_trying_delete_service_with_incorrect_service_id(client):
    response = client.delete('/api/service/5')
    assert response.status_code == 404


def test_trying_delete_service_with_orders(client):
    response = client.delete('/api/service/1')
    assert response.status_code == 409


def test_trying_delete_order_with_incorrect_order_id(client):
    response = client.delete('/api/order/5')
    assert response.status_code == 404
