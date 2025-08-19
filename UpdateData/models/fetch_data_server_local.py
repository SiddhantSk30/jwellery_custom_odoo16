from odoo import models, fields, api, _
import logging
import xmlrpc.client


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class InheritProduct(models.Model):
    _inherit = 'product.template'
    _description = "Inherit products form view & add new fields"

    def update_products_server_to_local(self):
        # Odoo server information
        odoo_url = 'http://157.245.108.79:8069'
        db_name = 'Torres14APR24'
        username = 'admin'
        password = 'OmSaiRam@1234#'

        # Initialize logging
        _logger = logging.getLogger(__name__)

        try:
            # Connect to the XML-RPC service
            common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
            uid = common.authenticate(db_name, username, password, {})
            _logger.info("\n\n\t\t action 1111111111 ========== %s %s", common, uid)

            # Connect to the XML-RPC service again with authenticated user
            models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')
            _logger.info("\n\n\t\t actio222222edit ========== %s %s", models, odoo_url)
            model_name = 'product.template'

            # Fetch product data from the server
            server_product_ids = models.execute_kw(db_name, uid, password, model_name, 'search', [[]])
            server_products = models.execute_kw(db_name, uid, password, model_name,
                                                'read', [server_product_ids],
                                                {'fields': ['name', 'code', 'list_price', 'standard_price']})

            for server_product_data in server_products:
                # Check if the product already exists locally
                existing_product = self.env['product.template'].search(
                    [('code', '=', server_product_data['code'])], limit=1)

                if existing_product:
                    # Update existing product in the local database
                    existing_product.write({
                        'list_price': server_product_data.get('list_price'),
                        'standard_price': server_product_data.get('standard_price')
                    })
                    _logger.info(f"\n\n\t\t Product '{server_product_data['name']}' updated locally.")
                else:
                    # Create new product in the local database
                    new_product = self.env['product.template'].create({
                        'name': server_product_data.get('name'),
                        'code': server_product_data.get('code'),
                        'list_price': server_product_data.get('list_price'),
                        'standard_price': server_product_data.get('standard_price')
                    })
                    _logger.info(f"\n\n\t\t New product '{server_product_data['name']}' created locally.")

        except Exception as e:
            _logger.error(f"\n\n\t\t Error updating products in the local database: {e}")
            return False

        return True

    # def update_products_server_to_local(self):
    #     # Odoo server information
    #     odoo_url = 'http://157.245.108.79:8069'
    #     db_name = 'Torres14APR24'
    #     username = 'admin'
    #     password = 'OmSaiRam@1234#'
    #
    #     # Initialize logging
    #     _logger = logging.getLogger(__name__)
    #
    #     try:
    #         # Connect to the XML-RPC service
    #         common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
    #         uid = common.authenticate(db_name, username, password, {})
    #         _logger.info("\n\n\t\t action 1111111111 ========== %s %s", common, uid)
    #
    #         # Connect to the XML-RPC service again with authenticated user
    #         models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')
    #         _logger.info("\n\n\t\t actio222222edit ========== %s %s", models, odoo_url)
    #         model_name = 'product.template'
    #
    #         # Fetch product data from the server
    #         server_product_ids = models.execute_kw(db_name, uid, password, model_name,
    #                                                'search', [[]])
    #         server_products = models.execute_kw(db_name, uid, password, model_name,
    #                                             'read', [server_product_ids],
    #                                             {'fields': ['name', 'code']})
    #
    #         for server_product_data in server_products:
    #             # Check if the product already exists locally
    #             product_data = server_product_data.read()[0]
    #
    #             existing_product = self.env['product.template'].search(
    #                 [('name', '=', server_product_data['name']), ('code', '=', server_product_data['code'])], limit=1)
    #
    #             if existing_product:
    #                 # Update existing product in the local database
    #                 existing_product.write(product_data)
    #                 _logger.info(f"\n\n\t\t Product '{server_product_data['name']}' updated locally.")
    #             else:
    #                 # Create new product in the local database
    #                 new_product = self.env['product.template'].create(product_data)
    #                 _logger.info(f"\n\n\t\t New product '{server_product_data['name']}' created locally.")
    #
    #     except Exception as e:
    #         _logger.error(f"\n\n\t\t Error updating products in the local database: {e}")
    #         return False
    #
    #     return True
