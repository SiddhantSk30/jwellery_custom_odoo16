from odoo import models, fields
from datetime import datetime, time, date, timedelta


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

   