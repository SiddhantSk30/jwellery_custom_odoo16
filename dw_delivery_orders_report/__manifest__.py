{
    'name': 'Delivery Order Reports',
    'version': '1.0',
    'summary': 'Custom reports for delivery orders',
    'description': """
    This module provides custom reports for delivery orders in Odoo.
    """,
    'author': 'Manoj Thombare',
    'category': 'Reporting',
    'depends': ['base', 'stock','product'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir.model.data.xml',
        'views/delivery_order_report_views.xml',
        'report/delivery_order_report.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
