from odoo import models, fields, api, _



class InheritPartner(models.Model):
   _inherit = 'res.partner'
   _description = "Inherit res partner form view & add new fields"
   _order = 'pan_no desc'
   
   pan_no = fields.Char(string="PAN No")
   #mobile =  fields.Char(string="Mobile",required=True)
   #street = fields.Char(required=True)
   #city = fields.Char(required=True)
   
   
