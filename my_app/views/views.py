import datetime
from json import JSONEncoder, dumps, loads
from flask import render_template, request, url_for, redirect, flash, Blueprint, jsonify
from flask_paginate import Pagination

from my_app.views.forms import AddClientForm, AddServiceForm, OrderFormSet, AddOrderForm
from my_app.views.requests_to_api import *

web_app = Blueprint('web', __name__, url_prefix='/my_app')


@web_app.context_processor
def inject_today_date():
    return {'today_date': datetime.date.today()}


@web_app.route("/clients")
def get_clients_list():
    date_from = request.args.get("date_from") or None
    date_by = request.args.get("date_by") or None
    page = request.args.get("page", 1)

    if date_from is None and date_by is None:
        response = get_list_of_items(f'/clients?page={page}')
    else:
        payload = {'date_from': date_from, 'date_by': date_by, 'page': page}
        response = get_list_of_filtering_items('/clients_filtering', payload)

        if response.status_code != 200:
            flash(response.json().get('message'), 'message_failure')
            return redirect(url_for('web.get_clients_list'))

    clients = response.json()
    pagination = Pagination(page=clients['page'],
                            per_page=clients['per_page'],
                            total=clients['total'])

    context = {'title': 'clients', 'heading': 'Clients list',
               'items_list': clients['items'], 'pagination': pagination, 'page': page}

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
            flash(message, 'message_success')
            return redirect(url_for('web.get_clients_list'))

        form = AddClientForm(data=data)
        form.phone_number.errors = [response.json().get('message')]

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
            flash(message, 'message_success')
            return redirect(url_for('web.get_clients_list'))

        form = AddClientForm(data=data)
        form.phone_number.errors = [response.json().get('message')]
    context = {'title': 'edit_client', 'form': form, 'heading': 'Edit client'}
    return render_template('add_or_change_client.html', context=context)


@web_app.route('/delete_client/<client_id><page>')
def delete_client(client_id, page):
    response = delete_item(f'/client/{client_id}')

    if response.status_code == 204:
        flash('Client deleted successfully', 'message_success')
    else:
        message = response.json().get('message')
        flash(message, 'message_failure')
    return redirect(url_for('web.get_clients_list', page=page))


@web_app.route("/services")
def get_services_list():
    price_from = request.args.get('price_from')
    price_by = request.args.get('price_by')
    page = request.args.get('page', 1)

    if price_from is None and price_by is None:
        response = get_list_of_items(f'/services?page={page}')
    else:
        response = get_list_of_filtering_items(
            '/services_filtering', {'price_from': price_from, 'price_by': price_by, 'page': page})

        if response.status_code != 200:
            flash(response.json().get('message'), 'message_failure')
            return redirect(url_for('web.get_services_list'))

    services = response.json()
    pagination = Pagination(page=services['page'],
                            per_page=services['per_page'],
                            total=services['total'])

    context = {'title': 'services', 'heading': 'Services list',
               'items_list': services['items'], 'pagination': pagination, 'page': page}

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
            flash(message, 'message_success')
            return redirect(url_for('web.get_services_list'))

        form = AddServiceForm(data=data)
        form.name.errors = [response.json().get('message')]

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
            flash(message, 'message_success')
            return redirect(url_for('web.get_services_list'))

        form = AddServiceForm(data=data)
        form.name.errors = [response.json().get('message')]
    context = {'title': 'edit_service', 'heading': 'Edit service', 'form': form}
    return render_template('add_or_change_service.html', context=context)


@web_app.route('/delete_service/<service_id><page>')
def delete_service(service_id, page):
    response = delete_item(f'/service/{service_id}')

    if response.status_code == 204:
        flash('Service deleted successfully', 'message_success')
    else:
        message = response.json().get('message')
        flash(message, 'message_failure')
    return redirect(url_for('web.get_services_list', page=page))


@web_app.route("/orders")
def get_orders_list():
    date_from = request.args.get('date_from') or None
    date_by = request.args.get('date_by') or None
    page = request.args.get('page', 1)

    if date_from is None and date_by is None:
        response = get_list_of_items(f'/orders?page={page}')
    else:
        payload = {'date_from': date_from, 'date_by': date_by, 'page': page}
        response = get_list_of_filtering_items('/orders_filtering', payload)

        if response.status_code != 200:
            flash(response.json().get('message'), 'message_failure')
            return redirect(url_for('web.get_orders_list'))
    orders = response.json()
    pagination = Pagination(page=orders['page'],
                            per_page=orders['per_page'],
                            total=orders['total'])

    context = {'title': 'orders', 'heading': 'Orders list',
               'items_list': orders['items'], 'pagination': pagination, 'page': page}

    return render_template('orders_list.html', context=context)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.isoformat()


def fill_select_fields_in_order_form(form):
    service_id_choices = list(map(
        lambda service: (service.get('id'), service.get('name')),
        get_list_of_items('/services/names').json()))

    client_id_choices = list(map(
        lambda client: (client.get('id'), client.get('phone_number')),
        get_list_of_items('/clients/phones').json()))

    form.client_id.choices = client_id_choices

    for sub_form in form.order_line:
        sub_form.service_id.choices.extend(service_id_choices)

    return form, service_id_choices


@web_app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    form = OrderFormSet()
    form, service_id_choices = fill_select_fields_in_order_form(form)

    AddOrderForm.Meta.created_date = form.created_date.data
    if form.is_submitted() and form.order_line.validate(AddOrderForm):
        payloads = {'created_date': form.created_date.data,
                    'client_id': form.client_id.data, 'order_lines': form.order_line.data}
        response = create_item('/orders', data=dumps(payloads, cls=CustomJSONEncoder))

        if response.status_code == 201:
            message = response.json().get('message')
            flash(message, 'message_success')
            return redirect(url_for('web.get_orders_list'))
        else:
            flash(response.json().get('message'), 'message_failure')
    else:
        [flash(line, 'message_failure') for line in form.errors.get('order_line', '') if len(line) != 0]

    context = {'title': 'add_order', 'form': form, 'heading': 'Add order',
               'add_line': True}
    return render_template('add_or_edit_order.html', context=context)


def object_hook(obj):
    date_field = "event_date" if "event_date" in obj else "created_date" if "created_date" in obj else None
    obj[date_field] = datetime.datetime.strptime(obj[date_field], '%Y-%m-%d').date()
    return obj


@web_app.route('/edit_order/<order_id>', methods=['GET'])
def edit_order_get(order_id):
    form = OrderFormSet()
    form, service_id_choices = fill_select_fields_in_order_form(form)

    form.order_line.pop_entry()
    response = get_item(f'/order/{order_id}')

    if response.status_code == 200:
        order = loads(response.text, object_hook=object_hook)

        dates_of_services_not_yet_performed = []

        for index, order_line in enumerate(order.get('order_lines')):
            order_line.update(get_unit_and_price_for_service(order_line.get('service_id')))
            form.order_line.append_entry(order_line)

            if order_line.get('event_date') < datetime.date.today():

                form.order_line.entries[index].form.quantity.render_kw = {'readonly': True}
                form.order_line.entries[index].form.event_date.render_kw = {'readonly': True}
                form.order_line.entries[index].form.service_id.render_kw = {'class': 'order-read-only-field'}
            else:
                dates_of_services_not_yet_performed.append(order_line.get('event_date'))

            for sub_form in form.order_line:
                sub_form.service_id.choices.extend(service_id_choices)

        form.created_date.data = order.get('created_date')
        form.created_date.render_kw = {'readonly': True}
        form.client_id.data = str(order.get('client_id'))

        context = {'title': 'edit_order', 'form': form, 'heading': 'Edit order',
                   'client_id': order.get('client_id'),
                   'add_line': len(dates_of_services_not_yet_performed) > 0}

        return render_template('add_or_edit_order.html', context=context)

    context = {'title': 'edit_order', 'heading': 'Edit order', 'main_page': 'get_orders_list'}
    return render_template('404.html', context=context)


@web_app.route('/edit_order/<order_id>', methods=['POST'])
def edit_order_post(order_id):
    form = OrderFormSet()
    form, service_id_choices = fill_select_fields_in_order_form(form)

    AddOrderForm.Meta.created_date = form.created_date.data
    if form.is_submitted() and form.order_line.validate(AddOrderForm):
        payload = {'created_date': form.created_date.data, 'client_id': form.client_id.data,
                   'order_lines': form.order_line.data}
        response = update_item(f'/order/{order_id}', data=dumps(payload, cls=CustomJSONEncoder))

        if response.status_code == 201:
            message = response.json().get('message')
            flash(message, 'message_success')
            return redirect(url_for('web.get_orders_list'))
    else:
        [flash(line, 'message_failure') for line in form.errors.get('order_line', '') if len(line) != 0]

    context = {'title': 'edit_order', 'form': form, 'heading': 'Edit order',
               'add_line': form.created_date.data >= datetime.date.today()}
    return render_template('add_or_edit_order.html', context=context)


def get_unit_and_price_for_service(service_id):
    response = get_item(f'/service/{service_id}').json()
    unit_and_price = {'unit': response.get('unit'), 'price': response.get('price')}
    return unit_and_price


@web_app.route('/unit_and_price/<service_id>')
def get_unit_and_price_for_js_order_line(service_id):
    result = get_unit_and_price_for_service(service_id)
    return jsonify({'unit': {'unit': result.get('unit')}, 'price': {'price': result.get('price')}})


@web_app.route('/delete_order/<order_id><page>')
def delete_order(order_id, page):
    response = delete_item(f'/order/{order_id}')
    if response.status_code == 204:
        flash('Order deleted successfully', 'message_success')
    else:
        message = response.json().get('message')
        flash(message, 'message_failure')
    return redirect(url_for('web.get_orders_list', page=page))
