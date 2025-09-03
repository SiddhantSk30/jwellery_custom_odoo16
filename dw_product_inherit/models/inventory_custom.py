from odoo import models, api
from lxml import etree

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """Override to make fields editable for internal transfers, deliveries, and returns."""
        res = super(StockMoveLine, self).fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type in ('form', 'tree') and self.env.context.get('picking_type_id'):
            picking_type = self.env['stock.picking.type'].browse(self.env.context['picking_type_id'])
            # Make fields editable for internal, outgoing, and incoming operations
            if picking_type.code in ('internal', 'outgoing', 'incoming'):
                doc = etree.XML(res['arch'])
                fields_to_edit = ['product_id', 'lot_id', 'qty_done', 'location_id', 'location_dest_id']
                for field in fields_to_edit:
                    nodes = doc.xpath(f"//field[@name='{field}']")
                    for node in nodes:
                        node.set('readonly', '0')
                        node.set('force_save', '1')
                res['arch'] = etree.tostring(doc, encoding='unicode')
        return res