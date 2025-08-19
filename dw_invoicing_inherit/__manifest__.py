{
    'name' : 'Custom Invoice',
    'version':'1.0.0',
    'author':'Dreamwarez',    
    'website':'www.dreamwarez.in',  
    'description': "This module is developed to do some custom functionalities in Invoice module",
    'category': 'Invoicing',
    'sequence': -90,
    'depends' : ['base','account'],          
    'data':['security/ir.model.access.csv',
            'reports/paperformat.xml',
            'views/invoice_inherit_view.xml',
            'views/newreport.xml',
            'views/temp.xml',
            ],
    'installable':True, 
    'auto-install':False,
    'application':True,
    'license' :'LGPL-3',
    'assets':{}
}



# Code Author: [Vaibhav Dhokchaule]
# Date: [28/12/2023]
# Description: [Inherit Account Move Model and did some customizations]
# Version: [ V16 ]
