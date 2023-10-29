import datetime
from json import JSONEncoder, dumps, loads
from flask import render_template, request, url_for, redirect, flash, Blueprint, jsonify
from flask_paginate import Pagination, get_page_args
from my_app.views.forms import AddClientForm, AddServiceForm, OrderFormSet, AddOrderForm
from my_app.views.requests_to_api import *

web_app = Blueprint('web', __name__, url_prefix='/my_app')


def get_page_data(data: list, offset: int = 0, per_page: int = 3) -> list:
    """select data on specified prices.

    Keyword arguments:
    data -- list of data;
    offset-- start index;
    per_page -- number of items per page.
    """
    return data[offset:offset+per_page]


def get_pagination_items(items_list):
    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
    total = len(items_list)
    items_list = get_page_data(data=items_list, offset=offset, per_page=10)
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return {'items_list': items_list, 'page': page, 'per_page': per_page, 'pagination': pagination}


@web_app.route("/clients")
def get_clients_list():
    date_1 = request.args.get("date_1") or None
    date_2 = request.args.get("date_2") or None
    if date_1 is None and date_2 is None:
        response = get_list_of_items('/clients')
    else:
        payload = {'date_1': date_1, 'date_2': date_2}
        response = get_list_of_filtering_items('/clients_filtering', payload)
        if response.status_code != 200:
            flash(response.json().get('error'))
            return redirect(url_for('web.get_clients_list'))
    clients_list = response.json()
    pagination_items = get_pagination_items(clients_list)
    context = {'title': 'clients', 'heading': 'Clients list'}
    context.update(pagination_items)
    return render_template('clients_list.html', context=context)


@web_app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = AddClientForm()
    if form.validate_on_submit():

        data = {'name': form.name.data,
                'phone_number': form.phone_number.data,
                'email': form.email.data}

        response = create_item('/clients', json=data)
        if response.status_code == 201:
            message = response.json().get('message')
            context = {'title': 'success', 'message': message, 'main_page': 'get_clients_list'}
            return render_template('success.html', context=context)
        form = AddClientForm(data=data)
        form.phone_number.errors = [response.json().get('error')]
    context = {'title': 'add_client', 'form': form, 'heading': 'Add client'}
    return render_template('add_or_change_client.html', context=context)


@web_app.route('/edit_client/<client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    if request.method == 'GET':
        response = get_item(f'/client/{client_id}')
        if response.status_code == 200:
            client = response.json()
            form = AddClientForm(data=client)
            context = {'title': 'edit_client', 'form': form}
            return render_template('add_or_change_client.html', context=context)
        context = {'title': 'edit_client', 'heading': 'Edit client', 'main_page': 'get_clients_list'}
        return render_template('404.html', context=context)
    form = AddClientForm()
    if form.validate_on_submit():
        data = {'name': form.name.data,
                'phone_number': form.phone_number.data,
                'email': form.email.data}

        response = update_item(f'/client/{client_id}', json=data)
        if response.status_code == 201:
            message = response.json().get('message')
            context = {'title': 'success', 'message': message, 'heading': 'Edit client', 'main_page': 'get_clients_list'}
            return render_template('success.html', context=context)
        form = AddClientForm(data=data)
        form.phone_number.errors = [response.json().get('error')]
    context = {'title': 'edit_client', 'form': form, 'heading': 'Edit client'}
    return render_template('add_or_change_client.html', context=context)


@web_app.route('/delete_client/<client_id>', methods=['GET'])
def delete_client(client_id):
    response = delete_item(f'/client/{client_id}')
    if response.status_code == 204:
        context = {'title': 'success', 'heading': 'Delete client',
                   'message': f'Record  with id={client_id} deleted successfully', 'main_page': 'get_clients_list'}
        return render_template('success.html', context=context)
    error = response.json().get('error')
    context = {'title': 'delete_service', 'heading': 'Delete service', 'main_page': 'get_clients_list'}
    if error:
        context['error'] = error
    return render_template('404.html', context=context)


@web_app.route("/services")
def get_services_list():
    price_1 = request.args.get('price_1') or None
    price_2 = request.args.get('price_2') or None
    if price_1 is None and price_2 is None:
        response = get_list_of_items('/services')
    else:
        response = get_list_of_filtering_items('/services_filtering', {'price_1': price_1, 'price_2': price_2})
        if response.status_code != 200:
            flash(response.json().get('error'))
            return redirect(url_for('web.get_services_list'))
    services_list = response.json()
    pagination_items = get_pagination_items(services_list)
    context = {'title': 'services', 'heading': 'Services list'}
    context.update(pagination_items)
    return render_template('services_list.html', context=context)


@web_app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():

        data = {'name': form.name.data, 'description': form.description.data,
                'unit': form.unit.data, 'price': form.price.data}

        response = create_item('/services', json=data)
        if response.status_code == 201:
            message = response.json().get('message')
            context = {'title': 'success', 'heading': 'Add service', 'message': message,
                       'main_page': 'get_services_list'}
            return render_template('success.html', context=context)

        form = AddServiceForm(data=data)
        form.name.errors = [response.json().get('error')]
    context = {'title': 'add_service', 'form': form, 'heading': 'Add service'}
    return render_template('add_or_change_service.html', context=context)


@web_app.route('/edit_service/<service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if request.method == 'GET':
        response = get_item(f'/service/{service_id}')
        if response.status_code == 200:
            service = response.json()
            form = AddServiceForm(data=service)
            context = {'title': 'edit_service', 'heading': 'Edit service', 'form': form}
            return render_template('add_or_change_service.html', context=context)
        context = {'title': 'edit_service', 'heading': 'Edit service', 'main_page': 'get_services_list'}
        return render_template('404.html', context=context)
    form = AddServiceForm()
    if form.validate_on_submit():
        data = {'name': form.name.data, 'description': form.description.data,
                'unit': form.unit.data, 'price': form.price.data}
        response = update_item(f'/service/{service_id}', json=data)
        if response.status_code == 201:
            message = response.json().get('message')
            context = {'title': 'success', 'heading': 'Edit service', 'message': message,
                       'main_page': 'get_services_list'}
            return render_template('success.html', context=context)

        form = AddServiceForm(data=data)
        form.name.errors = [response.json().get('error')]
    context = {'title': 'edit_service', 'heading': 'Edit service', 'form': form}
    return render_template('add_or_change_service.html', context=context)


@web_app.route('/delete_service/<service_id>', methods=['GET'])
def delete_service(service_id):
    response = delete_item(f'/service/{service_id}')
    if response.status_code == 204:
        context = {'title': 'success', 'heading': 'Delete service', 'main_page': 'get_services_list',
                   'message': f'Record  with id={service_id} deleted successfully'}
        return render_template('success.html', title='success', context=context)
    error = response.json().get('error')
    context = {'title': 'delete_service', 'heading': 'Delete service', 'main_page': 'get_services_list'}
    if error:
        context['error'] = error
    return render_template('404.html', context=context)


@web_app.route("/orders")
def get_orders_list():
    date_1 = request.args.get('date_1') or None
    date_2 = request.args.get('date_2') or None
    if date_1 is None and date_2 is None:
        response = get_list_of_items('/orders')
    else:
        payload = {'date_1': date_1, 'date_2': date_2}
        response = get_list_of_filtering_items('/orders_filtering', payload)
        if response.status_code != 200:
            flash(response.json().get('error'))
            return redirect(url_for('web.get_orders_list'))
    orders_list = response.json()
    pagination_items = get_pagination_items(orders_list)
    context = {'title': 'orders', 'heading': 'Orders list'}
    context.update(pagination_items)
    return render_template('orders_list.html', context=context)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.isoformat()


@web_app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    form = OrderFormSet()
    service_id_choices = [(i.get('id'), i.get('name'))
                          for i in get_list_of_items('/services').json()]
    client_id_choices = [(i.get('id'), i.get('phone_number'))
                         for i in get_list_of_items('/clients').json()]
    form.client_id.choices = client_id_choices
    for sub_form in form.order_line:
        sub_form.service_id.choices = service_id_choices
    result = get_unit_and_price_for_service(service_id_choices[0][0])

    AddOrderForm.Meta.created_date = form.created_date.data
    if form.is_submitted() and form.order_line.validate(AddOrderForm):
        payloads = {'created_date': form.created_date.data,
                    'client_id': form.client_id.data, 'services': form.order_line.data}
        response = create_item('/orders', data=dumps(payloads, cls=CustomJSONEncoder))
        if response.status_code == 201:
            message = response.json().get('message')
            context = {'title': 'success', 'message': message, 'heading': 'Add order', 'main_page': 'get_orders_list'}
            return render_template('success.html', context=context)

    script_url_without_parameter = request.url_root + 'my_app/unit_and_price/'

    context = {'title': 'add_order', 'form': form, 'unit': str(result.get('unit', 0)),
               'service_id': service_id_choices[0][0], 'price': result.get('price', 0),
               'heading': 'Add order', 'script_url_without_parameter': script_url_without_parameter}
    return render_template('add_or_edit_order.html', context=context)


def object_hook(obj):
    date_field = "event_date" if "event_date" in obj else "created_date" if "created_date" in obj else None
    obj[date_field] = datetime.datetime.strptime(obj[date_field], '%Y-%m-%d')
    return obj


@web_app.route('/edit_order/<order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    form = OrderFormSet()
    service_id_choices = [(i.get('id'), i.get('name')) for i in get_list_of_items('/services').json()]
    client_id_choices = [(i.get('id'), i.get('phone_number')) for i in get_list_of_items('/clients').json()]
    form.client_id.choices = client_id_choices
    service_id = service_id_choices[0][0]
    result = get_unit_and_price_for_service(service_id)
    script_url_without_parameter = request.url_root + 'my_app/unit_and_price/'
    for sub_form in form.order_line:
        sub_form.service_id.choices = service_id_choices
    if request.method == 'GET':
        form.order_line.pop_entry()
        response = get_item(f'/order/{order_id}')
        if response.status_code == 200:
            order = loads(response.text, object_hook=object_hook)
            for order_line in order.get('order_lines'):
                order_line.update(get_unit_and_price_for_service(order_line.get('service_id')))
                form.order_line.append_entry(order_line)
                for sub_form in form.order_line:
                    sub_form.service_id.choices = service_id_choices
            form.created_date.data = order.get('created_date')
            form.client_id.data = str(order.get('client_id'))
            form.client_id.choices = client_id_choices
            context = {'title': 'edit_order', 'form': form, 'unit': str(result.get('unit', 0)),
                       'service_id': service_id, 'price': result.get('price', 0), 'heading': 'Edit order',
                       'client_id': order.get('client_id'), 'script_url_without_parameter': script_url_without_parameter}
            return render_template('add_or_edit_order.html', context=context)
        context = {'title': 'edit_order', 'heading': 'Edit order', 'main_page': 'get_orders_list'}
        return render_template('404.html', context=context)

    AddOrderForm.Meta.created_date = form.created_date.data
    if form.is_submitted() and form.order_line.validate(AddOrderForm):
        payload = {'created_date': form.created_date.data, 'client_id': form.client_id.data,
                   'services': form.order_line.data}
        response = update_item(f'/order/{order_id}', data=dumps(payload, cls=CustomJSONEncoder))

        if response.status_code == 201:
            message = response.json().get('message')
            context = {'title': 'success', 'message': message, 'heading': 'Edit order', 'main_page': 'get_orders_list'}
            return render_template('success.html', context=context)
    context = {'title': 'edit_order', 'form': form, 'heading': 'Edit order'}
    return render_template('add_or_edit_order.html', context=context)


def get_unit_and_price_for_service(service_id):
    response = get_item(f'/service/{service_id}').json()
    unit_and_price = {'unit': response.get('unit'), 'price': response.get('price')}
    return unit_and_price


@web_app.route('/unit_and_price/<service_id>')
def get_unit_and_price_for_js_order_line(service_id):
    result = get_unit_and_price_for_service(service_id)
    return jsonify({'unit': {'unit': result.get('unit')}, 'price': {'price': result.get('price')}})


@web_app.route('/delete_order/<order_id>')
def delete_order(order_id):
    response = delete_item(f'/order/{order_id}')
    if response.status_code == 204:
        context = {'title': 'success',
                   'heading': 'Delete order',
                   'message': f'Record  with id={order_id} deleted successfully', 'main_page': 'get_orders_list'}
        return render_template('success.html', context=context)
    context = {'title': 'delete_order', 'heading': 'Delete order', 'main_page': 'get_orders_list'}
    return render_template('404.html', context=context)




