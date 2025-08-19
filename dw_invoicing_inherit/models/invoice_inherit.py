from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError, ValidationError, UserError
from datetime import datetime, time, date, timedelta
import json
from num2words import num2words
from odoo.tools.date_utils import get_month, get_fiscal_year
from odoo.tools.misc import format_date
import re
from collections import defaultdict


class InheritInvoiceLine(models.Model):
   _inherit = 'account.move.line'
   _description = "Inherit invoicing line to add po reference field"
   
   adv_paid_rs = fields.Float(string='Advance Paid Rs')
   
   # @api.depends("total")
   # def _compute_total(self):
   #    for rec in self:
   #       rec.total = rec.basic_freight + rec.local_collection  + rec.lr_charges + rec.door_delivery + rec.hamali + rec.other
      



class InheritInvoice(models.Model):
   _inherit = 'account.move'
   _description = "Inherit invoicing invoices form view & add new fields"

   order_nm = fields.Char(string='Order No')
   bill_amt_rs = fields.Float(string="Bill Amount (Rs)")
   cash_disc_rs = fields.Float(string="Cash Discount (Rs)")
   inv_amt = fields.Float(string="Invoice Amount")
   bill_type = fields.Selection([('credit','CREDIT'),('debit','DEBIT'),('other','OTHER')], string="Bill Type")
   order_date = fields.Date(string="Order Date")
   delivery_date = fields.Date("Delivery Date")
   balance_rs = fields.Float(string="Balance Rs")
   ptype = fields.Selection([('gold','Gold'),('silver','Silver'),('diamond','Diamond')],string="Product")
   purity = fields.Selection([('bis 916','BIS 916'),('bis 915','BIS 915'),('bis 914','BIS 914')])
   time_type = fields.Selection([('morning','Morning'),('evening','Evening')],string="Time")
   stone = fields.Char(string="Stone")
   net_weight = fields.Float(string="Net Weight(Gms)")
   wastage_gms = fields.Float(string="Wastage (Gms)")
   wastage = fields.Integer(string="Wastage %")
   initial = fields.Char(string="Initial")
   size = fields.Char(string="Size")
   description = fields.Text(string="Description") 
   mc_piece_rs = fields.Integer(string="MC / Piece(Rs)")
   mc_weight_gm = fields.Integer(string="MC / Weight(Gm)")
   store_amt_rs = fields.Float(string="Store Amount (Rs)")