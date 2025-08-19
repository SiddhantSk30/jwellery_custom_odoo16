# -*- coding: utf-8 -*-
{
    'name': "Fetch And Update Data of Server",
    'summary': "fetch data from db",
    'description': "fetch data from another db",
    'author': "Vikash Tiwari",
    'category': 'Fetch Data',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'dw_product_inherit'],
    # always loaded
    'data': [
        'views/fetch_data_local_server.xml',
        'views/fetch_data_server_local.xml',
    ],
    'license': 'OPL-1',

}
