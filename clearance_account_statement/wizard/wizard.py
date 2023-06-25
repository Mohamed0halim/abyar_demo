# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json


class JournalItemsWizard(models.TransientModel):
    _name = "bill.wizard"


    start_date = fields.Date('Start Period', required=True, readonly=False)
    end_date = fields.Date('End Period', required=True, readonly=False)
    # compute = '_compute_start_date_end_date',
    # custom_choose = fields.Selection(string="Choose partner", selection=[('all', 'All'), ('one', 'One Account'), ], required=True)
    the_partner_id = fields.Many2one('res.partner', required=True, readonly=False, tracking=True, string='The partner')

    # all_inv = fields.Boolean(string="No Period")


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

    # def get_clearance_account_statement_vendor_bill_report(self):
    #     domain = []
    #     done_append_ids = []
    #     product_returns_data = []
    #     list_data_dollar = []
    #     list_data = []
    #     # print('account_ids=======', self.the_partner_id.id, self.start_date)
    #     # if data['form']['the_partner_ids']:
    #     if self.the_partner_id.id:
    #         domain.append(('partner_id.id', '=', self.the_partner_id.id))
    #         domain.append(('move_type', '=', 'in_invoice'))
    #     # if data['form']['date_from']:
    #     if self.start_date:
    #         # print('datattttttttttttt==', data['form']['date_from'])
    #         domain.append(('invoice_date', '>=', self.start_date))
    #     # if data['form']['date_to']:
    #     if self.end_date:
    #         # print('datattttttttttttt==', data['form']['date_to'])
    #         domain.append(('invoice_date', '<=', self.end_date))
    #     # print('domain==', domain)
    #     move_lines = self.env['account.move'].search(domain)
    #     # print('all_accounts=======', move_lines)
    #     # print('len=move_lines===', len(move_lines))
    #     # all_inv = move_lines.mapped('currency_id')
    #     # print('all_inv***', all_inv)
    #     total_all = 0
    #     total_amount_residual = 0
    #     total_payment = 0
    #
    #     total_all_dollar = 0
    #     total_payment_dollar = 0
    #     total_amount_residual_dollar = 0
    #
    #     for account in move_lines:
    #         # print('currency_id=', account.currency_id.name)
    #         # print('tax_totals_json', account.tax_totals_json)
    #         # print('invoice_payments_widget', account.invoice_payments_widget)
    #         # print('amount_residual', account.amount_residual)
    #         if account.currency_id.name == 'USD':
    #             total_all_dollar += account.amount_total
    #             if account.invoice_payments_widget:
    #                 res = json.loads(account.invoice_payments_widget)
    #                 if res:
    #                     for i in res['content']:
    #                         # print('i', i['amount'])
    #                         total_payment_dollar += i['amount']
    #             total_amount_residual_dollar += account.amount_residual
    #
    #         # else: # remove else
    #         if account.currency_id.name == 'IQD':
    #             #     print('amount_total', account.amount_total)
    #             # account_data = move_lines.filtered(lambda line: line.account_id == account)
    #             # print('account_data',account_data)
    #             # total_all = sum(account.mapped('amount_total'))
    #             total_all += account.amount_total
    #             if account.invoice_payments_widget:
    #
    #                 res = json.loads(account.invoice_payments_widget)
    #                 if res:
    #                     for i in res['content']:
    #                         # print('i', i['amount'])
    #                         total_payment += i['amount']
    #             total_amount_residual += account.amount_residual
    #             # print('total_all', total_all, 'total_payment', total_payment, 'total_amount_residual',
    #             #       total_amount_residual)
    #     # for_partner_id = self.env['res.partner'].search([('id', '=', data['form']['the_partner_ids'])])
    #     vals = {
    #         'total_all': total_all,
    #         'total_payment': total_payment,
    #         'total_amount_residual': total_amount_residual,
    #         'total_all_dollar': total_all_dollar,
    #         'total_payment_dollar': total_payment_dollar,
    #         'total_amount_residual_dollar': total_amount_residual_dollar,
    #         'partner': self.the_partner_id.name,
    #         'from': self.start_date,
    #         'to': self.end_date,
    #     }
    #     list_data.append(vals)
    #     data = {
    #         'move_lines': list_data,
    #     }
    #     # print('list_data==', list_data)
    #     # print('data==', data)
    #     return self.env.ref('custom_detailed_account_statement.custom_detailed_account_statement_report_action').report_action(self, data=data)


    # report with details
    def get_clearance_account_statement_vendor_bill_report(self):
        domain = []
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
        for account in move_lines:
            total_receipts = 0
            total_receipts_quant = 0
            total_fees = 0
            # total_fees_quant = 0
            total_fees_and_receipts_quant = 0
            # print('currency_id=', account.currency_id.name)
            # print('tax_totals_json', account.tax_totals_json)
            # print('invoice_payments_widget', account.invoice_payments_widget)
            custom_date = account.invoice_date
            name_of_product = account.custom_product_id.name
            num_of_cars = account.num_of_cars
            # print('amount_residual', account.amount_residual)
            if account.invoice_line_ids:
                for l in account.invoice_line_ids:
                    if l.fees_or_receipts == 'receipts':
                        total_receipts += l.price_unit
                        # total_receipts_quant += l.quantity
                    if l.fees_or_receipts == 'fees':
                        total_fees += l.price_unit
                        # total_fees_quant += l.quantity
                    total_fees_and_receipts_quant += l.quantity

            vals = {
                'total_fees_and_receipts_quant': total_fees_and_receipts_quant,
                'total_receipts': total_receipts,
                # 'total_receipts_quant': total_receipts_quant,
                'total_fees': total_fees,
                # 'total_fees_quant': total_fees_quant,
                'custom_date': custom_date,
                'num_of_cars': num_of_cars,
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
        return self.env.ref('clearance_account_statement.clearance_account_statement_report_action').report_action(self, data=data)

