from flask import request
from flask_restful import reqparse, Resource, fields, marshal_with

from rest_api.service.crud import *
from .validators import (
    validate_page_and_per_page,
    validate_list_of_order_lines,
    validate_dates
)
from .responses_format import (
    resource_with_pagination,
    resource_fields_for_orders
)


class OrdersList(Resource):

    @marshal_with(resource_with_pagination | {'items': fields.Nested(resource_fields_for_orders)})
    def get(self):
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        valid_page, valid_per_page = validate_page_and_per_page(page, per_page)
        return get_all_records(Order, page=valid_page, per_page=valid_per_page)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('created_date', type=str)
        parser.add_argument('client_id', type=int, help='client_id is required', required=True)
        parser.add_argument('order_lines', type=validate_list_of_order_lines, location='json', required=True)
        args = parser.parse_args()

        return create_new_order(args), 201


class FilteringOrdersList(Resource):

    @marshal_with(resource_with_pagination | {'items': fields.Nested(resource_fields_for_orders)})
    def get(self):
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        valid_page, valid_per_page = validate_page_and_per_page(page, per_page)

        date_from = request.args.get('date_from')
        date_by = request.args.get('date_by')
        validation_dates = validate_dates(date_from, date_by)
        if len(validation_dates) == 2:
            return filter_by_two_dates(Order, *validation_dates, page=valid_page, per_page=valid_per_page)
        return filter_by_date(Order, validation_dates[0], page=valid_page, per_page=valid_per_page)


class OrderRecord(Resource):
    @marshal_with(resource_fields_for_orders)
    def get(self, order_id):
        res = get_record(Order, order_id)
        return res

    def put(self, order_id):
        created_date = get_record(Order, order_id).created_date
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('client_id', type=int, help='client_id is required')
        parser.add_argument('order_lines', type=list, location='json')
        args = parser.parse_args()
        validate_list_of_order_lines(args.get('order_lines'), created_date)
        return change_order_record(order_id, args), 201

    def delete(self, order_id):
        return delete_record(Order, order_id), 204
