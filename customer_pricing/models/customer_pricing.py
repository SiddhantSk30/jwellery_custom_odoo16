from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class CustomerPricingConfig(models.Model):
    _name = 'customer.pricing.config'
    _description = 'Customer Pricing Configuration'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    pricing_line_ids = fields.One2many('customer.pricing.line', 'config_id', string="Product Pricing")
    note = fields.Text(string="Note")
    quotation_id = fields.Many2one('sale.order', string="Related Quotation")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('quotation_sent', 'Quotation Sent'),
        ('confirmed', 'Confirmed'),
    ], default='draft', string="Status")

    def action_generate_quotation(self):
        """Generate a new quotation based on pricing configuration"""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("Only draft configurations can generate quotations."))

        # Create sale order lines
        order_lines = []
        for line in self.pricing_line_ids:
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'price_unit': line.final_price / line.quantity if line.quantity else 0,
                'name': line.product_id.name,
            }))

        # Create the quotation
        quotation = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': order_lines,
            'customer_pricing_config_id': self.id,  # Link to pricing config
        })

        self.quotation_id = quotation.id
        self.state = 'quotation_sent'

        return {
            'name': _('Quotation'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': quotation.id,
            'view_mode': 'form',
            'target': 'current',
        }


class CustomerPricingLine(models.Model):
    _name = 'customer.pricing.line'
    _description = 'Customer Pricing Line'

    config_id = fields.Many2one('customer.pricing.config', string="Pricing Config", ondelete="cascade")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=1)
    discount_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('flat', 'Flat')
    ], string="Discount Type", required=True)
    discount_value = fields.Float(string="Discount")
    final_price = fields.Float(string="Final Price", compute="_compute_final_price", store=True)

    @api.depends('product_id', 'discount_type', 'discount_value', 'quantity')
    def _compute_final_price(self):
        for rec in self:
            base_price = rec.product_id.list_price or 0.0
            if rec.discount_type == 'flat':
                unit_price = base_price - rec.discount_value
            elif rec.discount_type == 'percentage':
                unit_price = base_price * (1 - (rec.discount_value / 100))
            else:
                unit_price = base_price
            rec.final_price = unit_price * rec.quantity

    @api.constrains('discount_type', 'discount_value')
    def _check_discount_validity(self):
        for rec in self:
            if rec.discount_value < 0:
                raise ValidationError("Discount cannot be negative.")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_pricing_config_id = fields.Many2one(
        'customer.pricing.config',
        string="Pricing Config"
    )

    commercial_partner_id = fields.Many2one(
        related='partner_id.commercial_partner_id',
        string='Commercial Entity',
        store=True
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_custom_price(self):
        if self.partner_id and not self.customer_pricing_config_id:
            return  # Placeholder: Add logic later if needed

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.customer_pricing_config_id:
                order.customer_pricing_config_id.state = 'confirmed'
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for order in self:
            if order.customer_pricing_config_id:
                order.customer_pricing_config_id.state = 'draft'
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_pricing_config_ids = fields.One2many(
        'customer.pricing.config',
        'partner_id',
        string="Customer Pricing Configurations"
    )

    quotation_ids = fields.One2many(
        'sale.order',
        'partner_id',
        string="Quotations",
        domain=[('state', 'in', ['draft', 'sent'])]
    )

    invoice_ids = fields.One2many(
        'account.move',
        'partner_id',
        string="Invoices",
        domain=[('move_type', '=', 'out_invoice')]
    )
