from odoo import models, fields, api
import xlrd
import logging
import base64
from io import BytesIO
_logger = logging.getLogger(__name__)
class ImportEPCWizard(models.TransientModel):
    _name = 'import.epc.wizard'
    _description = 'Import EPC Wizard'

    file = fields.Binary(string="Excel File")

    def import_epc_codes(self):
        product_obj = self.env['product.template']
        data_buffer = BytesIO(base64.b64decode(self.file))
        xls_data = xlrd.open_workbook(file_contents=data_buffer.getvalue())
        # xls_data = xlrd.open_workbook(file_contents=self.file)
        sheet = xls_data.sheet_by_index(0)
        
        for row in range(1, sheet.nrows):  # Assuming the first row is the header
            product_code = int(sheet.cell_value(row, 0))  # Assuming product code is in the first column
            epc_code = int(sheet.cell_value(row, 1))  # Assuming EPC code is in the second column
            # print("########",epc_code)
            product = product_obj.search([('code', '=', product_code)], limit=1)
            if product:
                print("#######",epc_code)
                product.write({'epc_code': epc_code})
                
            else:
                _logger.warning("Product with code %s not found", product_code)


        return {'type': 'ir.actions.act_window_close'}
