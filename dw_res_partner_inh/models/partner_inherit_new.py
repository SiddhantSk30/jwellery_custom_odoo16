from odoo import models, fields

class ResPartners(models.Model):
    _inherit = 'res.partner'


    aadhar_no = fields.Char(string="Aadhar No")
    passport_no = fields.Char(string="Passport Number")
    