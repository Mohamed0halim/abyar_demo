# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Line Views',
    'author': 'Odoo Bin',
    'company': 'Odoo Bin',
    'maintainer': 'Odoo Bin',
    'description': """ This module allow you to display sale/quotation line views.Sale order line view with custom filters
                        and group by options, sale order line view by list, form, kanban and graph view, and pivot view etc,
                        Filters and group by in sale order line view, Sale order line search view, sale order line graph view, sale 
                        order line pivot view,
                        """,
    'summary': """This module allow you to display sale/quotation line views-List/Tree, form, graph,search and pivot view,.Sale order line view with custom filters
                        and group by options""",
    'version': '15.0',
    "license": "OPL-1",
    'depends': ['sale_management'],
    'demo': [],
    'data': [
        'views/order_line_image.xml',
        'views/sale_order_line_tree_view.xml'
    ],
    'live_test_url': 'https://www.youtube.com/watch?v=f7d2lQbjpUc',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
