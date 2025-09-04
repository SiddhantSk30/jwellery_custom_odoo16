{
    'version':'1.0.0',
    'author':'Dreamwarez',    
    'website':'www.dreamwarez.in',  
    'name': 'Custom Products',
    'description': " This module is for custom field in products model",
    'category': 'Product',
    'sequence': -100,
    'depends' : ['base','product','stock'],                                    
    'data':[
            'security/ir.model.data.xml',
            'security/ir.model.access.csv',
            'views/product_inherit_view.xml',
            'views/code_seq.xml',
            'views/details.xml',
            'views/migration.xml',
            
            ],
    'assets': {'web.assets_backend': ['your_module_name/static/src/css/custom.css',],},
    'post_init_hook': 'post_init_hook',
    'installable':True,                                                                                      
    'auto_install':False,
    'application':True,
    'license' :'LGPL-3',
    'assets':{}
}


# Code Author: [Vaibhav Dhokchaule]
# Date: [28/12/2023]
# Description: [Inherit Product template Model and did some customizations]
# Version: [ V16 ]
