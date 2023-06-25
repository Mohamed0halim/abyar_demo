# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class generalAccountMoveInherit(models.Model):
  _inherit = 'account.move'


  name_of_bill = fields.Char(string="اسـم الفاتورة",required=False, )


class generalAccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'


    # fees_or2_receipts2 = fields.Selection(string="Fees Receipts",
    #                                       selection=[('receipts', 'Receipts'), ('fees', 'Fees')], required=False, )
    custom_date = fields.Date(string="Date", required=False, default=fields.date.today())
    custom_notes = fields.Char(string="نوع الصرف", required=False, )