import json
from odoo import http
from odoo.http import request, Response
import logging


_logger = logging.getLogger(__name__)


class MyController(http.Controller):

    # api for fetching all the shops of the store
    @http.route('/api/product_shops', type='http', auth='public', methods=['GET'], csrf=False)
    def get_product_shops(self):
        try:
            # Fetch all product shops
            product_shops = request.env['product.shop'].sudo().search([])

            # Prepare data in the required format
            shops_data = []
            for shop in product_shops:
                shops_data.append({
                    'shopName': shop.name,
                    'shopLocation': shop.location,
                    'shopId': shop.id
                })

            # Return data as JSON response
            response_data = {
                'status': 'success',
                'data': shops_data
            }

            return Response(
                json.dumps(response_data),
                status=200,
                mimetype='application/json'
            )

        except Exception as e:
            error_data = {
                'status': 'error',
                'message': str(e)
            }
            return Response(
                json.dumps(error_data),
                status=500,
                mimetype='application/json'
            )

# api for the fetching all the racks list
    @http.route('/api/product_rack', type='http', auth='public', methods=['GET'], csrf=False)
    def get_rack_numbers(self):
        try:
            # Fetching all racks
            racks = request.env['product.rack'].sudo().search([])

            # Preparing JSON data
            data = []
            for rack in racks:
                data.append({
                    'rackNumber': rack.name,
                    'rackId': rack.id
                })

            # Returning the data as JSON
            response_data = {
                'status': 'success',
                'data': data
            }

            return Response(
                json.dumps(response_data),
                status=200,
                mimetype='application/json'
            )

        except Exception as e:
            error_data = {
                'status': 'error',
                'message': str(e)
            }
            return Response(
                json.dumps(error_data),
                status=500,
                mimetype='application/json'
            )

# api for getting all the floors list
    @http.route('/api/product_floor', type='http', auth='public', methods=['GET'], csrf=False)
    def get_product_floors(self):
        try:
            # Fetch all product floors
            product_floors = request.env['product.floor'].sudo().search([])

            # Prepare the list to store the floor numbers
            floor_data = []
            for floor in product_floors:
                floor_data.append({
                    'floorNumber': floor.name,
                    'floorId': floor.id
                })

            # Return the floor data as JSON
            response_data = {
                'status': 'success',
                'data': floor_data
            }

            return Response(
                json.dumps(response_data),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            error_data = {
                'status': 'error',
                'message': str(e)
            }
            return Response(
                json.dumps(error_data),
                status=500,
                mimetype='application/json'
            )

# api for checking product avialability

    @http.route('/check_epc', type='json', auth='public', methods=['POST'], csrf=False)
    def check_epc_availability(self):
        try:
            # Parsing the incoming request data
            raw_data = request.httprequest.data
            data = json.loads(raw_data)
            _logger.info("Received request data: %s", data)

            # Extract input parameters
            shop_id = data.get('shop_id')
            floor_id = data.get('floor_id')
            rack_id = data.get('rack_id')
            epc_code = data.get('epc_code')

            # Validate mandatory parameters
            if not (shop_id and floor_id and rack_id and epc_code):
                return {
                    'error': 'Missing required parameters: shop_id, floor_id, rack_id, and/or epc_code.'
                }

            # Extracting last three characters of EPC code
            request_epc_suffix = epc_code[-3:].lower().strip()
            _logger.info("Request EPC suffix: %s", request_epc_suffix)

            # Searching products based on shop, floor, and rack
            products = request.env['product.template'].search([
                ('shop_location', '=', shop_id),
                ('floor_no', '=', floor_id),
                ('rack_no', '=', rack_id)
            ])
            _logger.info("Found %s product(s) for shop ID %s, floor ID %s, rack ID %s",
                         len(products), shop_id, floor_id, rack_id)

            available_count = 0
            missing_count = 0

            # EPC code matching logic
            for product in products:
                if product.epc_code:
                    database_epc_suffix = product.epc_code[-3:].lower().strip()
                    if database_epc_suffix == request_epc_suffix:
                        available_count += product.quantity
                    else:
                        missing_count += product.quantity
                else:
                    missing_count += product.quantity

            # Fetching additional details
            shop_name = request.env['product.shop'].sudo().browse(
                shop_id).name if shop_id else None
            floor_number = request.env['product.floor'].sudo().browse(
                floor_id).name if floor_id else None
            rack_number = request.env['product.rack'].sudo().browse(
                rack_id).name if rack_id else None

            # Preparing the response
            response_data = {
                'epc_code': epc_code,
                'available': available_count > 0,
                'available_count': available_count,
                'missing_count': missing_count,
                'shopName': shop_name,
                'floorNumber': floor_number,
                'rackNumber': rack_number
            }
            _logger.info("Response data: %s", response_data)
            return response_data

        except Exception as e:
            _logger.error(
                "An error occurred in check_epc_availability: %s", str(e), exc_info=True)
            return {
                'status': 'error',
                'message': str(e)
            }
