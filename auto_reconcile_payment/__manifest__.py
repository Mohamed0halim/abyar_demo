{
    "name": "Auto Reconcile Payment Multi Invoice For Customer and Vendor || Multiple Invoice Payment  ",
    "version": "15.2.2.2",
    "description": """
        Using this module you can pay multiple invoice payment in one click.
    """,
    "author" : "Mohammedm Saeed",
    'sequence': 1,
    "email": 'dev.barhish@gmail.com',
    "website":'',
    'category':"Accounting",
    'summary':"",
    "depends": [ 'base', "account",
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/multiinvoice_payment_view.xml'
    ],
    'qweb': [],
    "images": [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

