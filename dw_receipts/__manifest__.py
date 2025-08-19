{
    'name': 'Custom Receipts',
    'version': '1.0',
    'category': 'Inventory/Receipts',
    'summary': 'Manage receipts and inventory',
    'description': """
        This module allows you to manage receipts and inventory in Odoo.
        You can create receipts for incoming products and track inventory levels.
    """,
    'author': 'Manoj',
    'depends': ['base', 'stock','product'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir.model.data.xml',
        'views/dw_receipt_views.xml',
        'views/custom_delivery_document.xml'
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
