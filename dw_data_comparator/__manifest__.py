{
    'name': "Odoo Data Comparator",
    'summary': "Compare data within the Odoo system",
    'description': """
        This module provides functionality to compare data within the Odoo system.
        It allows users to upload an XLS file containing data and compare it with 
        data exported from the system, helping to identify discrepancies.
    """,
    'author': "Manoj Thombare",
    # 'website': "https://www.example.com",
    'category': 'Tools',
    'version': '1.0',
    'depends': ['base', 'product','stock'],  # List of dependencies
    'data': [
        'security/ir.model.access.csv',
        'security/ir.model.data.xml',
        'views/data_comparison_views.xml',  # XML file defining views
        'security/ir.model.access.csv',     # CSV file defining access control
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
