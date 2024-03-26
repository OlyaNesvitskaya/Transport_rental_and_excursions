from flask_restful import fields


class Date(fields.Raw):
    """Field for outputting date in format: '%Y-%m-%d' """

    def format(self, value):
        res = value.strftime('%Y-%m-%d')
        return res


class Number(fields.Raw):
    """Field for outputting client's number of orders """

    def format(self, value):
        return len(value)


resource_with_pagination = {
        'page': fields.Integer,
        'per_page': fields.Integer,
        'total': fields.Integer,
        'pages': fields.Integer
}


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






