from odoo import models, fields, api
import xlrd
import base64
from io import BytesIO
# from termcolor import colored
from odoo import models, fields

class DataComparison(models.TransientModel):
    _name = 'data.comparison'
    _description = 'Data Comparison'

    name = fields.Char(string="EPC Code")
    prod_name = fields.Char(string="Product Name")
    quantity_xls = fields.Float(string="Reader Quantity")
    quantity_odoo = fields.Float(string="System Quantity")
    # price_xls = fields.Float(string="Price (XLS)")
    # price_odoo = fields.Float(string="Price (Odoo)")
    

class DataComparisonWizard(models.TransientModel):
    _name = 'data.comparison.wizard'
    _description = 'Data Comparison Wizard'

    xls_file = fields.Binary(string="XLS File", required=True)
    

    def compare_data(self):
        data_buffer = BytesIO(base64.b64decode(self.xls_file))
        xls_data = xlrd.open_workbook(file_contents=data_buffer.getvalue())
        # Read XLS file
        # xls_data = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        sheet = xls_data.sheet_by_index(0)

        # Extract data from XLS
        xls_product_data = []
        for row in range(1, sheet.nrows):
            product_data = {
                'name': int((sheet.cell(row, 0).value), 16),
                'quantity': sheet.cell(row, 1).value,
                # 'price': sheet.cell(row, 2).value,
            }
            xls_product_data.append(product_data)
        
        odoo_product_data = self.env['product.template'].search([])

        # Combine Odoo system records and XLS records
        comparison_data = []
        for odoo_product in odoo_product_data:
            matched = False     
            for i in xls_product_data:
                if hex(i['name']) == odoo_product.epc_code:
                    comparison_data.append({
                        'name': odoo_product.epc_code,
                        'prod_name': odoo_product.name,
                        'quantity_xls': i['quantity'],
                        'quantity_odoo': odoo_product.qty_available,
                        # 'price_xls': i['price'],
                        # 'price_odoo': odoo_product.list_price,
                    })
                    matched = True
                    break
            if not matched: 
                comparison_data.append({
                        'name': odoo_product.epc_code,
                        'prod_name': odoo_product.name,
                        'quantity_xls': 0 ,
                        'quantity_odoo': odoo_product.qty_available,
                        # 'price_xls': i['price'],
                        # 'price_odoo': odoo_product.list_price,
                    })       
                    
        # Create records in DataComparison model
        DataComparison = self.env['data.comparison']
        for data in comparison_data:
            DataComparison.create(data)

        # Define action for viewing comparison data
        action = self.env.ref('dw_data_comparator.action_data_comparison').read()[0]
        return action
