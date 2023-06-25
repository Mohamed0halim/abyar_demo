# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CustomAccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'


    # fees_or_receipts = fields.Selection(selection=[('receipts', 'Receipts'), ('fees', 'Fees')], required=False, )
    how_many_cars = fields.Float(string="Num Of Cars",  required=False, )


class WeeklyAccountMoveInherit(models.Model):
    _inherit = 'account.move'

