# -*- coding: utf-8 -*-
{
    'name': "Purchase Automation",

    'summary': """
        This Module will help you to automate the purchase""",

    'description': """
        Using this module User can create a PO and on confirm click the receipt and bill will create automatically
    """,

    'license': 'LGPL-3',
    'author': "Brain Station 23",
    'website': "https://brainstation-23.com/",
    'category': 'Purchase',
    'version': '15.0.1.0.0',
    'depends': ['purchase', 'stock'],

    'data': [
        'views/setting.xml',
    ],
    'images': ['static/description/banner.gif'],
    'application': True,
    'installable': True,
    'support': 'support@brainstation-23.com',
}
