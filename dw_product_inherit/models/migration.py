from odoo import models, fields, api
from odoo.exceptions import ValidationError

SUPERUSER_ID = 2

class Migration(models.TransientModel):
    _name = 'jwellery_custom.migration'
    _description = 'Migration Helper'

    def migrate_products(self):
        # Find products without a location_id
        products = self.env['product.template'].search([('location_id', '=', False)])
        if not products:
            return {}
        # Create default hierarchy entries if they don't exist
        default_location = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        if not default_location:
            default_location = self.env['stock.location'].create({'name': 'Default Location', 'usage': 'internal'})
        default_floor = self.env['product.floor'].search([('location_id', '=', default_location.id)], limit=1)
        if not default_floor:
            default_floor = self.env['product.floor'].create({'name': 'Default Floor', 'location_id': default_location.id})
        default_rack = self.env['product.rack'].search([('floor_id', '=', default_floor.id)], limit=1)
        if not default_rack:
            default_rack = self.env['product.rack'].create({'name': 'Default Rack', 'floor_id': default_floor.id})
        default_row = self.env['product.row'].search([('rack_id', '=', default_rack.id)], limit=1)
        if not default_row:
            default_row = self.env['product.row'].create({'name': 'Default Row', 'rack_id': default_rack.id})
        default_pallet = self.env['product.pallet'].search([('row_id', '=', default_row.id)], limit=1)
        if not default_pallet:
            default_pallet = self.env['product.pallet'].create({'name': 'Default Pallet', 'row_id': default_row.id})
        # Update products with new hierarchy fields
        for product in products:
            product.write({
                'location_id': default_location.id,
                'floor_id': default_floor.id,
                'rack_id': default_rack.id,
                'row_id': default_row.id,
                'pallet_id': default_pallet.id,
            })
        return {}

def post_init_hook(cr, registry):
    """Run migration after module installation."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['jwellery_custom.migration'].create({}).migrate_products()
