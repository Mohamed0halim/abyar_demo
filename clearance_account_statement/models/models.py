# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# class AccountMoveLineInherit(models.Model):
#     _inherit = 'account.move.line'
#
#
#     fees_or_receipts = fields.Selection(selection=[('receipts', 'Receipts'), ('fees', 'Fees')], required=False, )
