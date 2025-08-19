# -*- coding: utf-8 -*-
{
    'name': "product_label",
    'author': "Dreamwarez",
    'website': "http://www.dreamwarez.in",
    'category': 'Uncategorized',
    'sequence': -80, 
    'version': '0.1',
    'license' :'LGPL-3',
    'depends': ['base', 'product','stock'],
    'data': [
             'security/ir.model.access.csv',
             'security/ir.model.data.xml',
             'views/views.xml',
             'wizard/import_epc_wizard_view.xml'
            ],
}
