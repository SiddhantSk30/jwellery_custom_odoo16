
{
    'name': "User Warehouse Restriction",
    'version': '16.0.2.0.0',
    'category': 'Warehouse',
    'summary': """Restrict Warehouses and location for users.""",
    'description': """This module helps you to restrict warehouse and stock 
     location for the specific users. So that users can only access the allowed
     warehouse and locations.""",
    'author': 'Manoj',
    'company': 'Dreamwarez IT Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['stock', 'stock_sms'],
    'data': [
        'security/user_warehouse_restriction_groups.xml',
        'security/user_warehouse_security.xml',
        'views/res_config_settings_views.xml',
        'views/stock_warehouse_views.xml',
        'views/res_users_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
