{
    'version':'1.0.0',
    'author':'Dreamwarez',    
    'website':'www.dreamwarez.in',  
    'name': 'Custom Partner',
    'description': " This module is for custom field in res partner model",
    'category': 'Partner',
    'sequence': -92,
    'depends' : ['base'],                                    
    'data':['security/ir.model.access.csv',
            'views/partner_inherit_view.xml'
            ],
    'installable':True,                                                                                      
    'auto-install':False,
    'application':True,
    'license' :'LGPL-3',
    'assets':{}
}

# Code Author: [Vaibhav Dhokchaule]
# Date: [28/12/2023]
# Description: [Inherit Res Partner Model and did some customizations]
# Version: [ V16 ]