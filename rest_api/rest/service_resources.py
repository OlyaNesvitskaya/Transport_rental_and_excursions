from flask import request
from flask_restful import reqparse, Resource, fields, marshal_with

from rest_api.service.crud import *
from .validators import (
    validate_page_and_per_page,
    validate_prices
)

from .responses_format import (
    resource_with_pagination,
    resource_fields_for_services
)
from ..log import logger


class ServicesList(Resource):
    @marshal_with(resource_with_pagination | {'items': fields.Nested(resource_fields_for_services)})
    def get(self):
        logger.info(f"Request method:{request.method}, path:{request.full_path}")
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        valid_page, valid_per_page = validate_page_and_per_page(page, per_page)
        return get_all_records(Service, valid_page, valid_per_page)

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='name is required', required=True)
        parser.add_argument('description', type=str, help='description is required', required=True)
        parser.add_argument('unit', type=str, help='unit is required', required=True)
        parser.add_argument('price', type=int, help='price is required and must be integer', required=True)
        args = parser.parse_args()

        return create_new_record(Service, args), 201


class ServicesNamesList(Resource):
    @marshal_with({'id': fields.Integer, 'name': fields.String})
    def get(self):
        return get_all_names(Service)


class ServiceRecord(Resource):

    @marshal_with(resource_fields_for_services)
    def get(self, service_id):
        return get_record(Service, service_id)

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

    @marshal_with(resource_with_pagination | {'items': fields.Nested(resource_fields_for_services)})
    def get(self):
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        valid_page, valid_per_page = validate_page_and_per_page(page, per_page)

        price_from = request.args.get('price_from')
        price_by = request.args.get('price_by')
        valid_prices = validate_prices(price_from, price_by)
        if len(valid_prices) == 2:
            return filter_within_a_given_price_range(Service, *valid_prices, page=valid_page, per_page=valid_per_page)
        return filter_by_price(Service, valid_prices[0], page=valid_page, per_page=valid_per_page)






