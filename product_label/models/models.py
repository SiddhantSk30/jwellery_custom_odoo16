# -*- coding: utf-8 -*-

from odoo import models, fields, api


class productTemplate(models.Model):
    _inherit = 'product.template'

    def _get_report_base_filename(self):
        name = self.name + '_'+self.barcode
        return name

    def get_product_price(self):
        return round(self.list_price)
