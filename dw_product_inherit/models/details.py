from odoo import models, fields

class StockLocation(models.Model):
    _inherit = 'stock.location'

    floor_ids = fields.One2many('product.floor', 'location_id', string='Floors')

class ProductPallet(models.Model):
    _name = 'product.pallet'
    _description = 'Product Pallet'

    name = fields.Char(string='Pallet Number', required=True)
    row_id = fields.Many2one('product.row', string='Row', required=True)
    product_ids = fields.One2many('product.template', 'pallet_id', string='Products')

class ProductRow(models.Model):
    _name = 'product.row'
    _description = 'Product Row'

    name = fields.Char(string='Row Number', required=True)
    rack_id = fields.Many2one('product.rack', string='Rack', required=True)
    pallet_ids = fields.One2many('product.pallet', 'row_id', string='Pallets')

class ProductRack(models.Model):
    _name = 'product.rack'
    _description = 'Product Rack'

    name = fields.Char(string='Rack Number', required=True)
    floor_id = fields.Many2one('product.floor', string='Floor', required=True)
    row_ids = fields.One2many('product.row', 'rack_id', string='Rows')

class ProductFloor(models.Model):
    _name = 'product.floor'
    _description = 'Product Floor'

    name = fields.Char(string='Floor Number', required=True)
    location_id = fields.Many2one('stock.location', string='Location', required=True)
    rack_ids = fields.One2many('product.rack', 'floor_id', string='Racks')