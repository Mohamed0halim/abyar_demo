# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'purchase_task',
    'version': '1.1',
    'author': 'Altaher Gafar',
    'summary': '',
    'sequence': 90,
    'description': """
    """,
    'category': '',
    'website': '',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_custom.xml'
    ],
    'demo': [
    ],
}
