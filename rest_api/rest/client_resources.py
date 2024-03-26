from flask import request
from flask_restful import reqparse, Resource, fields, marshal_with

from rest_api.service.crud import *
from .validators import (
    validate_page_and_per_page,
    validate_phone_number,
    validate_dates
)
from .responses_format import (
    resource_with_pagination,
    resource_fields_for_clients
)


class ClientsList(Resource):
    @marshal_with(resource_with_pagination | {'items': fields.Nested(resource_fields_for_clients)})
    def get(self):
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        valid_page, valid_per_page = validate_page_and_per_page(page, per_page)

        return get_all_records(Client, valid_page, valid_per_page)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('created_date', type=str)
        parser.add_argument('name', type=str, help='name is required', required=True)
        parser.add_argument('phone_number', type=validate_phone_number, help='phone number is required and should consist only digits', required=True)
        parser.add_argument('email', type=str, help='email is required', required=True)
        args = parser.parse_args()
        result = create_new_record(Client, args)
        return result, 201


class ClientsPhonesList(Resource):

    @marshal_with({'id': fields.Integer, 'phone_number': fields.String})
    def get(self):
        return get_all_phone_numbers(Client)


class ClientRecord(Resource):

    @marshal_with(resource_fields_for_clients)
    def get(self, client_id):
        result = get_record(Client, client_id)
        return result

    def put(self, client_id):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='name is required')
        parser.add_argument('phone_number', type=validate_phone_number, help='phone number should consist only digits')
        parser.add_argument('email', type=str, help='email is required')
        args = parser.parse_args()
        return change_record(Client, client_id, args), 201

    def delete(self, client_id):
        return delete_record(Client, client_id), 204


class FilteringClientsList(Resource):

    @marshal_with(resource_with_pagination | {'items': fields.Nested(resource_fields_for_clients)})
    def get(self):
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        valid_page, valid_per_page = validate_page_and_per_page(page, per_page)

        date_from = request.args.get('date_from')
        date_by = request.args.get('date_by')
        validation_dates = validate_dates(date_from, date_by)
        if len(validation_dates) == 2:
            return filter_by_two_dates(Client, *validation_dates, page=valid_page, per_page=valid_per_page)
        return filter_by_date(Client, validation_dates[0], page=valid_page, per_page=valid_per_page)

