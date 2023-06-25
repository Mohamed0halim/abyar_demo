# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class GeneralJournalItems(models.TransientModel):
    _name = "weekly.general"


    start_date = fields.Date('Start Period', required=True, readonly=False)
    end_date = fields.Date('End Period', required=True, readonly=False)
    the_partner_id = fields.Many2one('res.partner', required=True, readonly=False, string='The partner')
    name_of_invoice = fields.Char(required=False, )

    @api.model
    def default_get(self, fields):
        res = super(GeneralJournalItems, self).default_get(fields)
        # active_ids = self._context.get('active_ids', [])
        # active_model = self._context.get('active_model')
        if self.env.context.get('active_id'):
            current_record1 = self.env['account.move'].search([('id', '=', self.env.context.get('active_id'))])
            # current_record = self.env['account.move'].browse(self.env.context.get('active_id'))
            print('current_record1==', current_record1)
            # print('current_record==', current_record)
            if current_record1:
                res['the_partner_id'] = current_record1.partner_id.id
                res['name_of_invoice'] = current_record1.name_of_bill
        return res
    # all_inv = fields.Boolean(string="No Period")

    @api.onchange('the_partner_id')
    def _compute_start_date_end_date(self):
        for rec in self:
            if rec.the_partner_id:
                # get today's datetime
                input_dt = datetime.today()
                # print('Datetime is:', input_dt)
                res = input_dt.replace(day=1)
                # print('First day of a month:', res)
                resss = res.date() + relativedelta(day=7)
                # print only date
                # print('Only date:', res.date())
                rec.start_date = res.date()
                rec.end_date = resss
            else:
                rec.start_date = False
                rec.end_date = False

    # report with details
    def general_get_weekly_account_statement_vendor_bill_report(self):
        domain = []
        list_data = []
        lines_data = []
        last_balance = 0
        last_balance_date = ''
        current_amount = ''
        current_date = ''
        if self.env.context.get('active_id'):
            current_record1 = self.env['account.move'].search([('id', '=', self.env.context.get('active_id'))])
            if current_record1:
                current_amount = current_record1.amount_total
                current_date = current_record1.invoice_date
                last_inv_for_same_partner = self.env['account.move'].search(
                    [('id', '!=', self.env.context.get('active_id')),
                     ('partner_id.id', '=', current_record1.partner_id.id),
                     ('move_type', '=', 'in_invoice')
                     ],
                order='create_date DESC',
                limit=1)
                if last_inv_for_same_partner:
                    last_balance = last_inv_for_same_partner.final_customer_balance
                    last_balance_date = last_inv_for_same_partner.invoice_date
        if self.the_partner_id.id:
            domain.append(('partner_id.id', '=', self.the_partner_id.id))
            # domain.append(('move_type', '=', 'in_invoice'))
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        if self.end_date:
            domain.append(('date', '<=', self.end_date))
        move_lines = self.env['account.payment'].search(domain)
        total_for_amount = 0
        if move_lines:
            for p in move_lines:
                print('p.date=', p.date)
                total_for_amount += p.amount
                vals = {
                    'pay_date': p.date,
                    'pay_memo': p.ref,
                    'pay_amount': p.amount,
                }
                list_data.append(vals)
        else:
            raise UserError('There are No Payments in this period, please change it')
        data = {
            'invoice_lines': lines_data,
            'move_lines': list_data,
            'from': self.start_date,
            'to': self.end_date,
            'partner': self.the_partner_id.name,
            'name_of_invoice': self.name_of_invoice,
            'current_amount': current_amount,
            'current_date': current_date,
            'last_balance': last_balance,
            'last_balance_date': last_balance_date,
            'total_for_amount': total_for_amount,
        }
        # print('list_data==', list_data)
        return self.env.ref('general_weekly_account_statement_for_c.general_weekly_account_statement_report_action').report_action(self, data=data)
