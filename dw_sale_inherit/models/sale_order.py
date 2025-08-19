from odoo import models, fields
from datetime import datetime, time, date, timedelta


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

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
    
    
    
    # outstanding_details = fields.Text(string='Outstanding Details')
    # agent_id = fields.Many2many('agent.details', string='Agent Details')
    # court_id = fields.Many2many('court.details', string='Court Details')
    # document_file = fields.Binary(string='Property Document')
    # loan_id = fields.Many2one('loan.details', string="Loan Borrower")
    # document_line_ids = fields.One2many('sale.document','document_id',string="Documents")


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    adv_paid_rs = fields.Float(string='Advance Paid Rs')
    
    # product_id = fields.Many2one(string='Property Name')
    # product_uom_qty = fields.Float(string='Guntha')
    # price_unit = fields.Float(string='Cost')
    # gatno = fields.Char(related="product_id.gat_no",string='Gat No')
    # area = fields.Char(related="product_id.area",string="Area")

# class SaleDocument(models.Model):
#     _name = 'sale.document'
#     _description = 'Uploaded Documents'

#     name = fields.Char(string='Document Name', required=True)
#     file = fields.Binary(string='Document File')
#     description = fields.Text(string='Description')
#     document_id = fields.Many2one('sale.order' ,string="Documents")    

# class InvoiceLineInherit(models.Model):
#     _inherit = 'account.move.line'

#     product_id = fields.Many2one(string='Property Name')
#     quantity = fields.Float(string='Guntha')