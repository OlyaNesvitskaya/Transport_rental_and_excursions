from flask import request
from flask_restful import reqparse, Resource, fields, marshal_with
from rest_api.service.crud import *
from rest_api.rest.validation import *


class Date(fields.Raw):
    """Field for outputting date in format: '%Y-%m-%d' """

    def format(self, value):
        res = value.strftime('%Y-%m-%d')
        return res


class Number(fields.Raw):
    """Field for outputting client's number of orders """

    def format(self, value):
        return len(value)


resource_fields_for_clients = {
    'id': fields.Integer,
    'name': fields.String,
    'phone_number': fields.String,
    'email': fields.String,
    'created_date': Date,
    'number_of_orders': Number(attribute='orders')
}

resource_fields_for_services = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'unit': fields.String,
    'price': fields.Integer,
    'number_of_orders': fields.Integer
}

order_line_fields = {
    'id': fields.Integer,
    'order_id': fields.Integer,
    'service_id': fields.Integer,
    'quantity': fields.Integer,
    'order_line_price': fields.Integer,
    'event_date': Date

}

resource_fields_for_orders = {
    'id': fields.Integer,
    'created_date': Date,
    'client_id': fields.Integer,
    'client_name': fields.String(attribute="client.name"),
    'total_price': fields.Integer(attribute='total_order_price'),
    'order_lines': fields.Nested(order_line_fields)
}


class ClientsList(Resource):
    @marshal_with(resource_fields_for_clients)
    def get(self):
        return get_all_records(Client)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('created_date', type=str)
        parser.add_argument('name', type=str, help='name is required', required=True)
        parser.add_argument('phone_number', type=validation_phone_number, help='phone number is required and should consist only digits', required=True)
        parser.add_argument('email', type=str, help='email is required', required=True)
        args = parser.parse_args()
        result = create_new_record(Client, args)
        return result, 201


class ClientRecord(Resource):

    @marshal_with(resource_fields_for_clients)
    def get(self, client_id):
        result = get_record(Client, client_id)
        return result

    def put(self, client_id):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='name is required')
        parser.add_argument('phone_number', type=validation_phone_number, help='phone number should consist only digits')
        parser.add_argument('email', type=str, help='email is required')
        args = parser.parse_args()
        return change_record(Client, client_id, args), 201

    def delete(self, client_id):
        return delete_record(Client, client_id), 204


class FilteringClientsList(Resource):

    @marshal_with(resource_fields_for_clients)
    def get(self):
        date_1 = request.args.get('date_1')
        date_2 = request.args.get('date_2')
        result = validate_dates(date_1, date_2)
        if len(result) == 2:
            return filter_by_two_dates(Client, *result)
        return filter_by_date(Client, result)


class ServicesList(Resource):
    @marshal_with(resource_fields_for_services)
    def get(self):
        return get_all_records(Service)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='name is required', required=True)
        parser.add_argument('description', type=str, help='description is required', required=True)
        parser.add_argument('unit', type=str, help='unit is required', required=True)
        parser.add_argument('price', type=int, help='price is required and must be integer', required=True)
        args = parser.parse_args()

        return create_new_record(Service, args), 201


class ServiceRecord(Resource):

    @marshal_with(resource_fields_for_services)
    def get(self, service_id):
        res = get_record(Service, service_id)
        return res

    def put(self, service_id):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='name is required')
        parser.add_argument('description', type=str, help='description is required')
        parser.add_argument('unit', type=str, help='unit is required')
        parser.add_argument('price', type=int, help='price is required')
        args = parser.parse_args()
        return change_record(Service, service_id, args), 201

    def delete(self, service_id):
        return delete_record(Service, service_id), 204


class FilteringServicesList(Resource):

    @marshal_with(resource_fields_for_services)
    def get(self):
        price_1 = request.args.get('price_1')
        price_2 = request.args.get('price_2')
        res = validate_prices(price_1, price_2)
        return filter_by_price(Service, *res)


class OrdersList(Resource):

    @marshal_with(resource_fields_for_orders)
    def get(self):
        return get_all_records(Order)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('created_date', type=str)
        parser.add_argument('client_id', type=int, help='client_id is required', required=True)
        parser.add_argument('services', type=validate_list_of_services, location='json', help='Invalid services', required=True)
        args = parser.parse_args()
        res = create_new_order(args)
        return res, 201


class FilteringOrdersList(Resource):

    @marshal_with(resource_fields_for_orders)
    def get(self):
        date_1 = request.args.get('date_1')
        date_2 = request.args.get('date_2')
        result = validate_dates(date_1, date_2)
        if len(result) == 2:
            return filter_by_two_dates(Order, *result)
        return filter_by_date(Order, result)


class OrderRecord(Resource):
    @marshal_with(resource_fields_for_orders)
    def get(self, order_id):
        res = get_record(Order, order_id)
        return res

    def put(self, order_id):
        created_date = get_record(Order, order_id).created_date
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('client_id', type=int, help='client_id is required')
        parser.add_argument('services', type=list, location='json')
        args = parser.parse_args()
        validate_list_of_services(args.get('services'), created_date)
        return change_order_record(order_id, args), 201

    def delete(self, order_id):
        return delete_record(Order, order_id), 204








