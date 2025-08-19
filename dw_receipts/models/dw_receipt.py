from odoo import models, fields, api
import xlrd
import base64
from io import BytesIO
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class Receipt(models.Model):
    _name = 'custom.receipt'
    _description = 'Custom Receipt'

    name = fields.Many2one('res.partner',string='Receive From', required=True)
    date = fields.Date(string='Receipt Date', required=True, default=fields.Date.today())
    line_ids = fields.One2many('custom.receipt.line', 'receipt_id', string='Receipt Lines')

    import_file = fields.Binary(string="Import File")

    def import_data(self): 
        missing_products = []
        for rec in self:
            xls_data = xlrd.open_workbook(file_contents=base64.decodebytes(rec.import_file ))
            sheet = xls_data.sheet_by_index(0)  # Assuming the data is in the first sheet
            for row in range(1, sheet.nrows):  # Assuming first row is header
                product_identifier = sheet.cell_value(row, 0) # Assuming product identifier in first column
                quantity = sheet.cell_value(row, 1)  # Assuming quantity in second column
                product = self.env['product.template'].search([('code', '=', product_identifier)])
                if product:
                    # products = self.env['stock.quant'].search([('product_id', '=', product.name)])
                    
                    # if product:
                    new_quantity = product.qty_available + quantity
                    product.write({'qty_available':new_quantity})
                    # product.writeqty_available
                    print("******",product.qty_available)       
                # else:
                #     missing_products.append(product.code)        
        
        if missing_products:
            _logger.warning("The following products are missing: %s", ', '.join(missing_products))
                    # print("*****",quantity)
        # xls_data = xlrd.open_workbook(file_contents=base64.decodebytes(self.import_file ))
        # sheet = xls_data.sheet_by_index(0)  # Assuming the data is in the first sheet

        # move_vals = []
        # for row_index in range(1, sheet.nrows):
        #     move_vals.append({'product_code' : int(sheet.cell_value(row_index, 0)),  
        #     'quantity' : sheet.cell_value(row_index, 1)})
        # print("*******",move_vals)   
        # so_lines = []
        # for line in move_vals:
        #     product = self.env['product.template'].search([('code', '=', line.get('product_code'))], limit=1)
        #     so_lines.append({
        #         # 'product_ids': [(4, line.get('id'))] , 
        #         'product_id':product.name,
        #         'quantity':line.get('quantity'),
        #     })
        # # print("*******",so_lines)
        # # for lines in so_lines:
        # move = self.env['custom.receipt.line'].create({'receipt_id': self.id})
        # move.write({self.line_ids: [(0, 0, values) for values in so_lines]}) 
        #     # self.line_ids.product_id = lines.get('product_id')
        #     # self.line_ids.quantity = lines.get('quantity')
        #     # print("****",self.line_ids.product_id.name)  

        # return True
class ReceiptLine(models.Model):
    _name = 'custom.receipt.line'
    _description = 'Custom Receipt Line'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', required=True)
    receipt_id = fields.Many2one('custom.receipt', string='Receipt')

    # def update_stock(self):
    #     product_ids = self.env['product.product'].search([])
    #     for product in product_ids:
    #         # Update stock for each product as needed
    #         product.write({'qty_available': new_quantity})

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    shipping_date = fields.Date(string='Shipping Date')
    gross_weight = fields.Float(string='Gross Weight')
    delivery_address = fields.Char(string='Delivery Address')
    transporter_name = fields.Char(string='Transporter Name')
    received_from = fields.Char(string='Received From')
    total_done_quantity = fields.Float(
        string='Total Done Quantity',
        compute='_compute_total_done_quantity'
    )
    note = fields.Text(string='Note')

    def _compute_total_done_quantity(self):
        for picking in self:
            picking.total_done_quantity = sum(picking.move_ids_without_package.filtered(lambda x: x.state == 'done').mapped('quantity_done')) 
    
    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_set_to_done(self):
        self.write({'state': 'done'})
        self.date_done = self.scheduled_date   

    @api.onchange('partner_id')
    def _onchange_partner_id_set_delivery_address(self):
        """Auto-fill delivery_address from partner when partner is selected."""
        for rec in self:
            if rec.partner_id:
                # Use the partner's full address
                address_parts = filter(None, [
                    rec.partner_id.street,
                    rec.partner_id.street2,
                    rec.partner_id.city,
                    rec.partner_id.state_id.name if rec.partner_id.state_id else '',
                    rec.partner_id.zip,
                    rec.partner_id.country_id.name if rec.partner_id.country_id else ''
                ])
                rec.delivery_address = ', '.join(address_parts)
            else:
                rec.delivery_address = False