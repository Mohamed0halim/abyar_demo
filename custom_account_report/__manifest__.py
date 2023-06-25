# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custome Accounting Reports',
    'version': '1.0',
    'summary': 'Editing Accounting ',
    'description': "",
    'website': 'https://www.odoo.com/app/inventory',
    'depends': ['account', 'purchase', 'sale', 'stock'],
    'sequence': -100,
    'data': [
        'views/partner_view.xml',
        'data/account_financial_report_data.xml',

    ],
    'license': 'LGPL-3'

}
