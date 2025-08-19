from odoo import models, fields, api, _
import logging
import xmlrpc.client


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class InheritProduct(models.Model):
    _inherit = 'product.template'
    _description = "Inherit products form view & add new fields"

    def update_products_local_to_server(self):
        # Odoo server information
        odoo_url = 'http://157.245.108.79:8069'
        db_name = 'Torres14APR24'
        username = 'admin'
        password = 'OmSaiRam@1234#'

        try:
            # Connect to the XML-RPC service
            common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
            uid = common.authenticate(db_name, username, password, {})
            models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')
            model_name = 'product.template'

            # Fetch local product data
            local_products = self.env['product.template'].search([])
            print('--Product count ', len(local_products.ids))

            mismatch_pro = []
            match_pro = []

            for product in local_products:
                product_data = {
                    'name': product.name,
                    'list_price': product.list_price,
                    'standard_price': product.standard_price,
                    'code': product.code
                }

                # Search for existing product on the server by product code
                existing_product_ids = models.execute_kw(db_name, uid, password, model_name, 'search',
                                                         [[('code', '=', product.code)]], {'limit': 1})

                if existing_product_ids:
                    # Update existing product on the server
                    models.execute_kw(db_name, uid, password, model_name, 'write',
                                      [existing_product_ids, product_data])
                    _logger.info(f"Product '{product.name}' code '{product.code}' updated on the server.")
                    match_pro.append(product.id)
                else:
                    # Create new product on the server with local product data
                    new_product_id = models.execute_kw(db_name, uid, password, model_name,
                                                       'create', [product_data])
                    _logger.info(f"New product '{product.name}' created on the server with ID {new_product_id}")
                    mismatch_pro.append(product.id)

            print(mismatch_pro, '====mismatch_pro=====\n\n======match_pro', match_pro)
        except Exception as e:
            _logger.error(f"Error updating products on the server: {e}")
            return False

    # def update_products_local_to_server(self):
    #     # Odoo server information
    #     odoo_url = 'http://157.245.108.79:8069'
    #     db_name = 'Torres14APR24'
    #     username = 'admin'
    #     password = 'OmSaiRam@1234#'
    #
    #     try:
    #         # Connect to the XML-RPC service
    #         common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
    #         uid = common.authenticate(db_name, username, password, {})
    #         models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')
    #         model_name = 'product.template'
    #
    #         # Fetch local product data
    #         local_products = self.env['product.template'].search([])
    #         print('--local_products Product count ', len(local_products.ids))
    #
    #         mismatch_pro = []
    #         match_pro = []
    #
    #         # Fetch existing products from the server
    #         server_products = models.execute_kw(db_name, uid, password, model_name, 'search_read', [[]],
    #                                             {'fields': ['id', 'name', 'code', 'list_price', 'standard_price']})
    #
    #         # Create a dictionary for faster lookup
    #         server_products_dict = {product['name']: product for product in server_products}
    #         print('server_products product data  server_products_dict=\n\n', server_products)
    #         for product in local_products:
    #             product_data = {
    #                 'name': product.name,
    #                 'list_price': product.list_price,
    #                 'standard_price': product.standard_price
    #             }
    #             print('::local product_data::\n\n\n', product_data)
    #             if product.code in server_products_dict:
    #                 server_product = server_products_dict[product.code]
    #                 print(product_data, 'ifff------Who is Product need to update ------', server_product)
    #                 match_pro.append(product.id)
    #                 s_id = [server_product['id']]
    #                 # Update existing product on the server
    #                 models.execute_kw(db_name, uid, password, model_name, 'write',
    #                                   [[server_product['id']], product_data])
    #                 _logger.info(f"server product id {s_id} Product '{product.name}' code '{product.code}' updated on the server.")
    #             else:
    #                 mismatch_pro.append(product.id)
    #
    #                 # Create new product on the server with local product data
    #                 new_product_id = models.execute_kw(db_name, uid, password, model_name,
    #                                                    'create', [product_data])
    #                 _logger.info(f"ELSEEE  New product '{product.name}' created on the server with ID {new_product_id}")
    #
    #         print(mismatch_pro, '====mismatch_pro=====\n\n======match_pro', match_pro)
    #     except Exception as e:
    #         _logger.error(f"Error updating products on the server: {e}")
    #         return False
