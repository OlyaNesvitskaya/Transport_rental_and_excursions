from flask import Blueprint, jsonify
from flask_restful import Api

from .errors import InvalidAPIUsage
from .client_resources import ClientsList, FilteringClientsList, ClientsPhonesList, ClientRecord
from .service_resources import ServicesList, FilteringServicesList, ServicesNamesList, ServiceRecord
from .order_resources import OrdersList, FilteringOrdersList, OrderRecord

api_app = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_app)


@api_app.app_errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


api.add_resource(ClientsList, '/clients')
api.add_resource(ClientsPhonesList, '/clients/phones')
api.add_resource(FilteringClientsList, '/clients_filtering')
api.add_resource(ClientRecord, '/client/<client_id>')

api.add_resource(ServicesList, '/services')
api.add_resource(ServicesNamesList, '/services/names')
api.add_resource(FilteringServicesList, '/services_filtering')
api.add_resource(ServiceRecord, '/service/<service_id>')

api.add_resource(OrdersList, '/orders')
api.add_resource(FilteringOrdersList, '/orders_filtering')
api.add_resource(OrderRecord, '/order/<order_id>')
