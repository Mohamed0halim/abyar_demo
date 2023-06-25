# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class CustomAccountInheritMove(models.Model):
  _inherit = 'account.move'


  processing_or_clearance = fields.Selection(string="Type", selection=[('processing', 'Processing'),
                                                                       ('clearance', 'Clearance'), ],
                                             required=False, default="processing")
  inv_department = fields.Selection(string="Department", selection=[('finance_dept', 'Finance Dept')],
                                    required=False, default="finance_dept", readonly=True)
  inv_currency = fields.Selection(string="Currency", selection=[('u_s', 'United States Dollars')],
                                    required=False, default="u_s", readonly=True)

  contract_num = fields.Char(string="Contract Number", required=False)
  contract_titel = fields.Char(string="Contract Title", required=False)
  contact_person = fields.Char(required=False)
  gr_number = fields.Char(string="Gr No", required=False)
  service_order_no = fields.Char(required=False)
  description_of_services = fields.Char(required=False)
  Period_of_performance = fields.Char(required=False)

class CustomAccountMoveInheritLine(models.Model):
  _inherit = 'account.move.line'

  note = fields.Char(string="Note", required=False)
