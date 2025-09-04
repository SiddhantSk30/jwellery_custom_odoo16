from odoo import models, fields, api, _
from datetime import datetime
import logging
import requests

_logger = logging.getLogger(__name__)

class InheritProduct(models.Model):
    _inherit = 'product.template'
    _description = "Inherit products form view & add new fields"

    metal_type = fields.Selection(
        [('925', '925'), ('14K', '14K'), ('18K', '18K'), ('22K', '22K')], string='Metal Type')
    printer_name = fields.Selection(
        [("LAPTOP-6QQI50SJ/Printronix_Auto_ID_T820_-_PGL", "Printronix T820")],
        string="Printer",
        default="LAPTOP-6QQI50SJ/Printronix_Auto_ID_T820_-_PGL"
    )
    metal = fields.Selection(
        [('gold', 'Gold'), ('silver', 'Silver')], string='Metal')
    article = fields.Char(string='Article', compute='_generate_article_seq')
    location_id = fields.Many2one(
        'stock.location',
        string="Location",
        required=True,
        domain="[('usage', '=', 'internal')]",
        default=lambda self: self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
    )
    floor_id = fields.Many2one(
        'product.floor',
        string="Floor",
        required=True,
        domain="[('location_id', '=', location_id)]",
        default=lambda self: self.env['product.floor'].search([], limit=1)
    )
    rack_id = fields.Many2one(
        'product.rack',
        string="Rack",
        required=True,
        domain="[('floor_id', '=', floor_id)]",
        default=lambda self: self.env['product.rack'].search([], limit=1)
    )
    row_id = fields.Many2one(
        'product.row',
        string="Row",
        required=True,
        domain="[('rack_id', '=', rack_id)]",
        default=lambda self: self.env['product.row'].search([], limit=1)
    )
    pallet_id = fields.Many2one(
        'product.pallet',
        string="Pallet",
        required=True,
        domain="[('row_id', '=', row_id)]",
        default=lambda self: self.env['product.pallet'].search([], limit=1)
    )
    supplier_nme = fields.Char(string="Supplier Name")
    gross_wt = fields.Float(string="Gross Weight")
    net_weight = fields.Float(string="Net Weight")
    carrat = fields.Float(string="Carrat 1")
    pcs = fields.Float(string="Pcs 1")
    black_beads = fields.Float(string="Black Beads(CTS)")
    enamel = fields.Float(string="Enamel")
    stone_type = fields.Selection(
        [('dm', 'DM'), ('ms', 'MS'), ('cz', 'CZ')], string='Stone Type 1')
    arrival_date = fields.Date(string="Date Of Arrival")
    stone_type_two = fields.Selection(
        [('dm', 'DM'), ('ms', 'MS'), ('cz', 'CZ'), ('sps', 'SPS')], string='Stone Type 2')
    st_two_carrat = fields.Float(string="Carrat 2")
    st_two_pcs = fields.Float(string="Pcs 2")
    stone_type_three = fields.Selection(
        [('dm', 'DM'), ('ms', 'MS'), ('cz', 'CZ')], string='Stone Type 3')
    st_three_carrat = fields.Float(string="Carrat 3")
    st_three_pcs = fields.Float(string="Pcs 3")
    epc_code = fields.Char(
        string='EPC Code', compute='_compute_epc', readonly=True)
    barcode = fields.Char(
        string="Barcode", compute="_generate_custom_barcode", readonly=True)
    code = fields.Char(
        string='Product Code', readonly=True, copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('product.template'))
    invoice_policy = fields.Selection(
        [('order', 'Ordered quantities'),
         ('delivery', 'Delivered quantities')], string='Invoicing Policy',
        store=True, readonly=False,
        help='Ordered Quantity: Invoice quantities ordered by the customer.\n'
        'Delivered Quantity: Invoice quantities delivered to the customer.',
        groups="dw_product_inherit.group_fields_invisible")
    product_tag_ids = fields.Many2many(
        'product.tag', string='Product Tags', groups="dw_product_inherit.group_fields_invisible")
    l10n_in_hsn_code = fields.Char(
        string="HSN/SAC Code", help="Harmonized System Nomenclature/Services Accounting Code",
        groups="dw_product_inherit.group_fields_invisible")
    l10n_in_hsn_description = fields.Char(
        string="HSN/SAC Description", help="HSN/SAC description is required if HSN/SAC code is not provided.",
        groups="dw_product_inherit.group_fields_invisible")
    hide_carrat_on_label = fields.Boolean(
        string='Hide Carrat On Label', default=False)
    exe_file_path = fields.Char(string="Path to .exe file")
    shape = fields.Selection([
        ('round', 'Round'),
        ('heart', 'Heart'),
        ('emerald', 'Emerald'),
        ('trillion', 'Trillion'),
        ('oval', 'Oval'),
        ('princess', 'Princess'),
        ('pear', 'Pear'),
        ('radiant', 'Radiant'),
        ('asscher', 'Asscher'),
        ('marquise', 'Marquise'),
        ('cushion', 'Cushion'),
        ('triangle', 'Triangle'),
    ], string="Shape")
    rfid_code = fields.Integer(
        string='RFID Code', compute='_generate_rfid_tag', readonly=True, help='RFID code for the product')
    quantity = fields.Integer(string="Quantity")
    stock_quant_ids = fields.One2many(
        'stock.quant', compute='_compute_stock_quant_ids', string='Stock Quantities')
    total_internal_quantity = fields.Float(
        string="Total Internal Quantity", compute='_compute_total_internal_quantity', readonly=True)
    tracking = fields.Selection(
        [('none', 'No Tracking'), ('serial', 'By Unique Serial Number'), ('lot', 'By Lots')],
        string='Tracking', default='none',
        help="Enable tracking by lot or serial number for inventory management.")

    def _compute_stock_quant_ids(self):
        for product in self:
            quants = self.env['stock.quant'].search([
                ('product_id.product_tmpl_id', '=', product.id),
                ('location_id.usage', '=', 'internal')
            ])
            available_quants = quants.filtered(lambda q: q.quantity > 0)
            product.stock_quant_ids = available_quants

    def _compute_total_internal_quantity(self):
        for product in self:
            quants = self.env['stock.quant'].search([
                ('product_id.product_tmpl_id', '=', product.id),
                ('location_id.usage', '=', 'internal')
            ])
            product.total_internal_quantity = sum(quant.quantity for quant in quants)

    @api.depends('product_variant_ids', 'product_variant_ids.qty_available')
    def _compute_quantities(self):
        """Override qty_available to include all internal locations."""
        super(InheritProduct, self)._compute_quantities()
        for product in self:
            quants = self.env['stock.quant'].search([
                ('product_id.product_tmpl_id', '=', product.id),
                ('location_id.usage', '=', 'internal')
            ])
            product.qty_available = sum(quant.quantity for quant in quants)

    def _compute_epc(self):
        for rec in self:
            rec.epc_code = self.env['ir.sequence'].next_by_code('product.template.epc') or hex(rec.rfid_code)

    def execute_exe_file(self):
        metal_type = self.metal_type
        if metal_type:
            metal_type = str(self.metal_type)
        else:
            metal_type = " "
        carrat = self.hide_carrat_on_label
        if carrat:
            carat = "  "
        else:
            carat = "Carrat:" + str(self.carrat)
        if self.categ_id.name == 'Stone':
            template_file = "JewellaryTag_Stone.btw"
        else:
            template_file = "JewellaryTag.btw"
        bartender_api_url = 'https://ap1.bartendercloud.com/api/actions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpZYUVKd1R6RlYwa28ydTFCMjdoYSJ9.eyJodHRwczovL0JhclRlbmRlckNsb3VkLmNvbS9UZW5hbnRJRCI6IjFlNzczNTJjLWZkYTUtNGE2Ny05YzNjLTI2OGIyMDFkMjhlMCIsImh0dHBzOi8vQmFyVGVuZGVyQ2xvdWQuY29tL1VzZXJJRCI6IjFjMzI3Y2E3LTM1MmQtNDFjOC1iNTVkLWVmYjBlNzEwMjljZSIsImh0dHBzOi8vQmFyVGVuZGVyQ2xvdWQuY29tL0RhdGFDZW50ZXJVUkkiOiJodHRwczovL2FwMS5iYXJ0ZW5kZXJjbG91ZC5jb20vIiwiaXNzIjoiaHR0cHM6Ly9iYXJ0ZW5kZXJjbG91ZC1wcm9kdWN0aW9uLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjJjMDg0NDk0NGMwY2YyNWEwOWNhYmMiLCJhdWQiOlsiaHR0cHM6Ly9CYXJUZW5kZXJDbG91ZFNlcnZpY2VBcGkiLCJodHRwczovL2JhcnRlbmRlcmNsb3VkLXByb2R1Y3Rpb24udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcyNDc1MDEyOSwiZXhwIjoxNzI3MzQyMTI5LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIiwiYXpwIjoiVEM0c3dKbHMxd0lSOGpvSk1YWkZnd2tLSDBrblNpSG4iLCJwZXJtaXNzaW9ucyI6W119.Zyas8WuCHG3UXLIdXHsWXBrCKFqNf2SnVWVCDSC0QwjK6pRMsDemACJkpt7G0-a70LGdO0c8Nsx4omc1pklnDDLorDccmc5bLEw1KIsDjCRaYjeDN8F23t3Tq0nF-TZYsh9kHLAh4ONUfPWEpdARoDaMIS6QpH0hr-dPDPB_oXBwLHhptTS_8Nlihf_ONDT0pwmZiwGvkF6rV1W6kENO98Zbp75_824LSCM-DMb0hkHZsp5JTSmZd_sBIVNDR1_0Sfce9aIpKsxw0lSr-8Z120CHXmRuqmoafW0epAsuFcHWbxWeVS4GQEJ0Xmyllp0YNDppK6RDmF1h0AlO3xLkBA'
        }
        data = {
            "PrintBTWAction": {
                "DocumentFile": f"librarian://main/{template_file}",
                "Printer": f"printer:{self.printer_name}",
                "VerifyPrintJobIsComplete": True,
                "NamedDataSources": {
                    "price": "Price: " + str(self.list_price),
                    "grossWeight": "Gr Wt:" + str(self.gross_wt),
                    "carrat1": carat,
                    "productName": self.categ_id.name,
                    "stoneType": self.stone_type.upper() if self.stone_type else "",
                    "article": self.article,
                    "productCode": self.code,
                    "metalType": metal_type,
                    "rfid": self.code,
                    "barcode": self.code
                }
            }
        }
        try:
            response = requests.post(bartender_api_url, headers=headers, json=data)
            if response.status_code == 200:
                _logger.info("Label printed successfully.")
            else:
                _logger.error(f"Failed to print label: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error while connecting to Bartender: {str(e)}")

    def _generate_rfid_tag(self):
        for rec in self:
            try:
                rec.rfid_code = int(rec.code) if rec.code and rec.code.isdigit() else 0
            except ValueError:
                rec.rfid_code = 0
                _logger.warning(f"Cannot convert code '{rec.code}' to integer for RFID code")

    def _generate_article_seq(self):
        for rec in self:
            frt_scd_su_nme = rec.supplier_nme[:3].upper() if rec.supplier_nme else ""
            nme = rec.metal[0].upper() if rec.metal else ""
            categid_first_letter = rec.categ_id.name[0].upper() if rec.categ_id.name else ""
            categid_lst_letter = rec.categ_id.name[-1].upper() if rec.categ_id.name else ""
            stne_type = rec.stone_type.upper() if rec.stone_type else ""
            article_code = f"{frt_scd_su_nme}{nme}{categid_first_letter}{categid_lst_letter}{stne_type}"
            rec.article = article_code

    def _generate_custom_barcode(self):
        for rec in self:
            frt_scd_su_nme = rec.supplier_nme[:2].upper() if rec.supplier_nme else ""
            nme = rec.name[:7].upper() if rec.name else ""
            current_date = datetime.now()
            current_day_str = str(current_date.day)
            mnth = current_date.strftime('%m')
            barcode = f"{frt_scd_su_nme}{nme}{current_day_str}{mnth}"
            rec.barcode = barcode

    @api.model
    def create(self, vals):
        _logger.debug("Creating product with values: %s", vals)
        res = super(InheritProduct, self).create(vals)
        _logger.debug("Created product: %s", res.read(['location_id', 'floor_id', 'rack_id', 'row_id', 'pallet_id']))
        return res

    def write(self, vals):
        _logger.debug("Writing to product %s with values: %s", self.ids, vals)
        res = super(InheritProduct, self).write(vals)
        _logger.debug("Updated product: %s", self.read(['location_id', 'floor_id', 'rack_id', 'row_id', 'pallet_id']))
        return res

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    pro_code = fields.Char(string="Product Code", related='product_tmpl_id.code')

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    available_qty_corrected = fields.Float(
        string="Available (Corrected)",
        compute="_compute_available_corrected",
        store=False
    )

    def _compute_available_corrected(self):
        for quant in self:
            quant.available_qty_corrected = quant.quantity - quant.reserved_quantity
