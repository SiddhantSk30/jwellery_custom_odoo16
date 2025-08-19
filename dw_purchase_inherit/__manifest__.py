# -*- coding: utf-8 -*-
{
    'name': 'Custom Purchase Order',
    'version': '15.0.1.0.0',  # Module version
    'category': 'Purchase',
    'author': 'Dreamwarez',
    'website': 'https://www.Dreamwarez.in',
    'license': 'AGPL-3',  # License information
    'summary': 'Customizes the Sale module in Odoo',
    'sequence': -90,  # Show custom module on top sequence of app list
    'depends': [
        'base',  # Dependencies on other modules
        'sale'  # Example: This module depends on the Sale module
    ],
    'data': [
        
        'security/ir.model.access.csv',  # Access control file
        
        'views/newreport.xml',
        'views/temp.xml',
        'reports/paperformat.xml',
        
    ],
    'installable': True,  # Whether the module can be installed
    'application': True,  # Whether the module is an application
    'auto_install': False,  # Whether the module should be auto-installed
}


# Code Author: [Vaibhav Dhokchaule]
# Date: [28/12/2023]
# Description: [Inherit Sales Order Model and did some customizations]
# Version: [ V15 ]