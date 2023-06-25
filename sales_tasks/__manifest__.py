# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'M_sales_tasks',
    'version': '0.1',
    'summary': '',
    'sequence': 90,
    'description': """
    """,
    'category': '',

    'author': "Mohamed0halim",
    'website': "linkedin.com/in/mo-halim",

    'depends': ['base', 'sale' , 'sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_custom.xml',
        'views/invoice_for_sale_view.xml',
    ],
    'demo': [
    ],
}
