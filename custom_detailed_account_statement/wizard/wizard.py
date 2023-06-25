# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json


class JournalItemsWizard(models.TransientModel):
    _name = "journal.wizard"


    start_date = fields.Date('Start Period', required=True, readonly=False)
    end_date = fields.Date('End Period', required=True, readonly=False)
    # compute = '_compute_start_date_end_date',
    # custom_choose = fields.Selection(string="Choose partner", selection=[('all', 'All'), ('one', 'One Account'), ], required=True)
    the_partner_id = fields.Many2one('res.partner', required=True, readonly=False, tracking=True, string='The partner')

    all_inv = fields.Boolean(string="No Period")


    # @api.depends('start_date', 'end_date')
    @api.onchange('the_partner_id')
    def _compute_start_date_end_date(self):
        for rec in self:
            if rec.the_partner_id:
                # get today's datetime
                input_dt = datetime.today()
                # print('Datetime is:', input_dt)
                res = input_dt.replace(day=1)
                # print('First day of a month:', res)
                resss = res.date() + relativedelta(day=31)
                # print only date
                # print('Only date:', res.date())
                rec.start_date = res.date()
                rec.end_date = resss
            else:
                rec.start_date = False
                rec.end_date = False

    def get_general_account_statement_returns_report(self):
        domain = []
        done_append_ids = []
        product_returns_data = []
        list_data_dollar = []
        list_data = []
        # print('account_ids=======', self.the_partner_id.id, self.start_date)
        # if data['form']['the_partner_ids']:
        if self.the_partner_id.id:
            domain.append(('partner_id.id', '=', self.the_partner_id.id))
            domain.append(('move_type', '=', 'in_invoice'))
        # if data['form']['date_from']:
        if self.start_date:
            # print('datattttttttttttt==', data['form']['date_from'])
            domain.append(('invoice_date', '>=', self.start_date))
        # if data['form']['date_to']:
        if self.end_date:
            # print('datattttttttttttt==', data['form']['date_to'])
            domain.append(('invoice_date', '<=', self.end_date))
        # print('domain==', domain)
        move_lines = self.env['account.move'].search(domain)
        # print('all_accounts=======', move_lines)
        # print('len=move_lines===', len(move_lines))
        # all_inv = move_lines.mapped('currency_id')
        # print('all_inv***', all_inv)
        total_all = 0
        total_amount_residual = 0
        total_payment = 0

        total_all_dollar = 0
        total_payment_dollar = 0
        total_amount_residual_dollar = 0

        for account in move_lines:
            # print('currency_id=', account.currency_id.name)
            # print('tax_totals_json', account.tax_totals_json)
            # print('invoice_payments_widget', account.invoice_payments_widget)
            # print('amount_residual', account.amount_residual)
            if account.currency_id.name == 'USD':
                total_all_dollar += account.amount_total
                if account.invoice_payments_widget:
                    res = json.loads(account.invoice_payments_widget)
                    if res:
                        for i in res['content']:
                            # print('i', i['amount'])
                            total_payment_dollar += i['amount']
                total_amount_residual_dollar += account.amount_residual

            # else: # remove else
            if account.currency_id.name == 'IQD':
                #     print('amount_total', account.amount_total)
                # account_data = move_lines.filtered(lambda line: line.account_id == account)
                # print('account_data',account_data)
                # total_all = sum(account.mapped('amount_total'))
                total_all += account.amount_total
                if account.invoice_payments_widget:

                    res = json.loads(account.invoice_payments_widget)
                    if res:
                        for i in res['content']:
                            # print('i', i['amount'])
                            total_payment += i['amount']
                total_amount_residual += account.amount_residual
                # print('total_all', total_all, 'total_payment', total_payment, 'total_amount_residual',
                #       total_amount_residual)
        # for_partner_id = self.env['res.partner'].search([('id', '=', data['form']['the_partner_ids'])])
        vals = {
            'total_all': total_all,
            'total_payment': total_payment,
            'total_amount_residual': total_amount_residual,
            'total_all_dollar': total_all_dollar,
            'total_payment_dollar': total_payment_dollar,
            'total_amount_residual_dollar': total_amount_residual_dollar,
            'partner': self.the_partner_id.name,
            'from': self.start_date,
            'to': self.end_date,
        }
        list_data.append(vals)
        data = {
            'move_lines': list_data,
        }
        # print('list_data==', list_data)
        # print('data==', data)
        return self.env.ref('custom_detailed_account_statement.custom_detailed_account_statement_report_action').report_action(self, data=data)


    # report with details
    def get_report_with_details_returns_report(self):
        domain = []
        done_append_ids = []
        product_returns_data = []
        list_data_dollar = []
        list_data = []
        # print('account_ids=======', self.the_partner_id.id, self.start_date)
        # if data['form']['the_partner_ids']:
        if self.the_partner_id.id:
            domain.append(('partner_id.id', '=', self.the_partner_id.id))
            domain.append(('move_type', '=', 'in_invoice'))
        # if data['form']['date_from']:
        if self.start_date:
            # print('datattttttttttttt==', data['form']['date_from'])
            domain.append(('invoice_date', '>=', self.start_date))
        # if data['form']['date_to']:
        if self.end_date:
            # print('datattttttttttttt==', data['form']['date_to'])
            domain.append(('invoice_date', '<=', self.end_date))
        # print('domain==', domain)
        move_lines = self.env['account.move'].search(domain)
        total_all = 0
        total_all_dollar = 0
        custom_date = ''
        num_of_cars = 0
        # wrong place
        # total_paid_in_dollar = 0 # المبلغ الواصل بالدولار
        # total_paid = 0 # المبلغ الواصل بالدينار
        # unpaid_in_dollar = 0 # المتبقي بالدولار
        # unpaid_in = 0 # المتبقي بالدينار
        # vals = {}
        for account in move_lines:
            total_paid_in_dollar = 0  # المبلغ الواصل بالدولار
            total_paid = 0  # المبلغ الواصل بالدينار
            unpaid_in_dollar = 0  # المتبقي بالدولار
            unpaid_in = 0  # المتبقي بالدينار
            # print('currency_id=', account.currency_id.name)
            # print('tax_totals_json', account.tax_totals_json)
            # print('invoice_payments_widget', account.invoice_payments_widget)
            custom_date = account.invoice_date
            name_of_product = account.custom_product_id.name
            num_of_cars = account.num_of_cars
            # print('amount_residual', account.amount_residual)
            if account.currency_id.name == 'USD':
                total_all_dollar = account.amount_total
                if account.invoice_payments_widget:
                    res = json.loads(account.invoice_payments_widget)
                    if res:
                        for i in res['content']:
                            # print('i', i['amount'])
                            total_paid_in_dollar += i['amount']
                unpaid_in_dollar += account.amount_residual
                # print('total_paid_in_dollar==', total_paid_in_dollar, unpaid_in_dollar)
            else:
                total_all_dollar = 0
                total_paid_in_dollar = 0
                unpaid_in_dollar = 0
            # remove else
            # else:
            if account.currency_id.name == 'IQD':
                total_all = account.amount_total
                if account.invoice_payments_widget:
                    res = json.loads(account.invoice_payments_widget)
                    if res:
                        for i in res['content']:
                            # print('i', i['amount'])
                            total_paid += i['amount']
                unpaid_in += account.amount_residual
                # print('accounttotal_paid==', total_paid, unpaid_in, account)
            # for_partner_id = self.env['res.partner'].search([('id', '=', data['form']['the_partner_ids'])])
            else:
                total_paid = 0
                unpaid_in = 0
                total_all = 0
            vals = {
                'total_paid_in_dollar': total_paid_in_dollar,
                'total_paid': total_paid,
                'unpaid_in_dollar': unpaid_in_dollar,
                'unpaid_in': unpaid_in,
                'total_all': total_all,
                'custom_date': custom_date,
                'num_of_cars': num_of_cars,
                'total_all_dollar': total_all_dollar,
                'name_of_product': name_of_product,
                'partner': self.the_partner_id.name,
                'from': self.start_date,
                'to': self.end_date,
            }
        # print('vals==', vals)
            list_data.append(vals)
        data = {
            'move_lines': list_data,
            'from': self.start_date,
            'to': self.end_date,
            'partner': self.the_partner_id.name,
        }
        # print('list_data==', list_data)
        # print('data==', data)
        return self.env.ref('custom_detailed_account_statement.custom_with_details_statement_report_action').report_action(self, data=data)


    # no period
    def get_all_report_for_all_inv_paid(self):
        domain = []
        done_append_ids = []
        product_returns_data = []
        list_data_dollar = []
        list_data = []
        if self.the_partner_id.id:
            domain.append(('partner_id.id', '=', self.the_partner_id.id))
            domain.append(('move_type', '=', 'in_invoice'))
            domain.append(('payment_state', 'in', ('not_paid', 'partial')))
        move_lines = self.env['account.move'].search(domain)
        total_all = 0
        total_all_dollar = 0
        custom_date = ''
        num_of_cars = 0
        # total_paid_in_dollar = 0 # المبلغ الواصل بالدولار
        # total_paid = 0 # المبلغ الواصل بالدينار
        # unpaid_in_dollar = 0 # المتبقي بالدولار
        # unpaid_in = 0 # المتبقي بالدينار
        date_now = datetime.now()
        # print('date_now', date_now)
        # vals = {}
        for account in move_lines:
            total_paid_in_dollar = 0  # المبلغ الواصل بالدولار
            total_paid = 0  # المبلغ الواصل بالدينار
            unpaid_in_dollar = 0  # المتبقي بالدولار
            unpaid_in = 0  # المتبقي بالدينار

            custom_date = account.invoice_date
            name_of_product = account.custom_product_id.name
            num_of_cars = account.num_of_cars
            if account.currency_id.name == 'USD':
                total_all_dollar = account.amount_total
                if account.invoice_payments_widget:
                    res = json.loads(account.invoice_payments_widget)
                    if res:
                        for i in res['content']:
                            # print('i', i['amount'])
                            total_paid_in_dollar += i['amount']
                unpaid_in_dollar += account.amount_residual
                # print('total_paid_in_dollar==', total_paid_in_dollar, unpaid_in_dollar)
            else:
                total_all_dollar = 0
                total_paid_in_dollar = 0
                unpaid_in_dollar = 0
            if account.currency_id.name == 'IQD':
                total_all = account.amount_total
                if account.invoice_payments_widget:
                    res = json.loads(account.invoice_payments_widget)
                    if res:
                        for i in res['content']:
                            # print('i', i['amount'])
                            total_paid += i['amount']
                unpaid_in += account.amount_residual
                # print('accounttotal_paid==', total_paid, unpaid_in, account)
            else:
                total_paid = 0
                unpaid_in = 0
                total_all = 0
            vals = {
                'total_paid_in_dollar': total_paid_in_dollar,
                'total_paid': total_paid,
                'unpaid_in_dollar': unpaid_in_dollar,
                'unpaid_in': unpaid_in,
                'total_all': total_all,
                'custom_date': custom_date,
                'num_of_cars': num_of_cars,
                'total_all_dollar': total_all_dollar,
                'name_of_product': name_of_product,
                'partner': self.the_partner_id.name,
            }
        # print('vals', vals)
            list_data.append(vals)
        data = {
            'move_lines': list_data,
            'partner': self.the_partner_id.name,
            'date_now': date_now,
        }
        return self.env.ref('custom_detailed_account_statement.custom_report_for_all_no_period').report_action(self, data=data)
