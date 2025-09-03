from odoo import models, fields, api
from odoo.exceptions import ValidationError

SUPERUSER_ID = 2

class Migration(models.TransientModel):
    _name = 'jwellery_custom.migration'
    _description = 'Migration Helper'

    def migrate_products(self):
        # No hierarchy migration needed
        return {}

def post_init_hook(cr, registry):
    """Run migration after module installation."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['jwellery_custom.migration'].create({}).migrate_products()