from odoo import api, fields, models


class ResUsers(models.Model):
    """This model adds additional fields to the `res.users` model to restrict
     user access to certain locations and warehouses."""
    _inherit = 'res.users'

    restrict_location = fields.Boolean(string="Restrict Location",
                                       help='Restrict location for the user.')
    location_ids = fields.Many2many(comodel_name='stock.location',
                                    string='Restricted Locations',
                                    help='Restricted locations for users.')
    allowed_warehouse_ids = fields.Many2many(
        comodel_name='stock.warehouse', string='Allowed Warehouse',
        help='Allowed Warehouse for user.')
    check_user = fields.Boolean(string="Check", compute='_compute_check_user',
                                help="Indicates whether the user has warehouse"
                                     " location restrictions.")

    @api.model
    def create(self, vals):
        self.clear_caches()
        return super(ResUsers, self).create(vals)

    def write(self, vals):
        self.clear_caches()
        return super(ResUsers, self).write(vals)

    def _compute_check_user(self):
        """To determine if the user has warehouse location restrictions.
        Sets the check_user field accordingly."""
        restriction_group_id = self.env.ref(
            'user_warehouse_restriction.user_warehouse_restriction_group_user').id
        for record in self:
            record.check_user = False
            if restriction_group_id in record.groups_id.mapped('id'):
                record.check_user = True
