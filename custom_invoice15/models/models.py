# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,
                               states={'draft': [('readonly', False)]}, default=fields.date.today() )
