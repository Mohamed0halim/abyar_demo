# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class JournalItemsWizard(models.TransientModel):
    _name = "weekly.wizard"


    start_date = fields.Date('Start Period', required=True, readonly=False)
    end_date = fields.Date('End Period', required=True, readonly=False)
    the_partner_id = fields.Many2one('res.partner', required=True, readonly=False,
                                     string='The partner')
    name_of_invoice = fields.Char(required=False, )

    @api.model
    def default_get(self, fields):
        res = super(JournalItemsWizard, self).default_get(fields)
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
    def get_weekly_account_statement_vendor_bill_report(self):
        domain = []
        list_data = []
        lines_data = []
        last_balance = 0
        if self.env.context.get('active_id'):
            current_record1 = self.env['account.move'].search([('id', '=', self.env.context.get('active_id'))])
            if current_record1:
                # if current_record1.move_type == 'out_invoice':
                last_inv_for_same_partner = self.env['account.move'].search(
                    [('id', '!=', self.env.context.get('active_id')),
                     ('partner_id.id', '=', current_record1.partner_id.id),
                     ('move_type', '=', 'out_invoice')
                     ],
                order='create_date DESC',
                limit=1)
                # else:
                #     last_inv_for_same_partner = self.env['account.move'].search(
                #         [('id', '!=', self.env.context.get('active_id')),
                #          ('partner_id.id', '=', current_record1.partner_id.id),
                #          ('move_type', '=', 'in_invoice')
                #          ],
                #     order='create_date DESC',
                #     limit=1)
                # print('last_inv_for_same_partner==', last_inv_for_same_partner)
                # for r in last_inv_for_same_partner:
                #     print('create_date==', r.create_date, r)
                if last_inv_for_same_partner:
                    last_balance = last_inv_for_same_partner.final_customer_balance
                    if last_balance < 0:
                        last_balance = last_balance * -1
                    frac = last_balance - int(last_balance)
                    if frac < 0.5:
                        last_balance = int(last_balance)
                    else:
                        last_balance = last_balance

                # create_date
                # current_record = self.env['account.move'].browse(self.env.context.get('active_id'))
                # print('current_record1==', current_record1)
                # print('invoice_line_ids==', current_record1.invoice_line_ids)
                for l in current_record1.invoice_line_ids:
                    # print('===', l.product_id)
                    valss1 = {
                        'date': current_record1.invoice_date,
                        'custom_date': l.custom_date,
                        'product_id': l.product_id.name,
                        'how_many_cars': l.how_many_cars,
                        'quant': l.quantity,
                        'uom': l.product_uom_id.name,
                        'price': l.price_unit,
                        'price_subtotal': l.price_subtotal,
                    }
                    lines_data.append(valss1)
                # print('lines_data==', lines_data)
        if self.the_partner_id.id:
            domain.append(('partner_id.id', '=', self.the_partner_id.id))
            # domain.append(('move_type', '=', 'in_invoice'))
        # if data['form']['date_from']:
        if self.start_date:
            # print('datattttttttttttt==', data['form']['date_from'])
            domain.append(('date', '>=', self.start_date))
        # if data['form']['date_to']:
        if self.end_date:
            # print('datattttttttttttt==', data['form']['date_to'])
            domain.append(('date', '<=', self.end_date))
        # print('domain==', domain)
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
                    'total_for_amount': total_for_amount,
                }
                list_data.append(vals)
        else:
            raise UserError('There are No Payments in this period, please change it')
        # print('list_data==', list_data)
        data = {
            'invoice_lines': lines_data,
            'move_lines': list_data,
            'from': self.start_date,
            'to': self.end_date,
            'partner': self.the_partner_id.name,
            'name_of_invoice': self.name_of_invoice,
            'last_balance': last_balance,
        }
        # print('list_data==', list_data)
        return self.env.ref('weekly_account_statement.weekly_account_statement_report_action').report_action(self, data=data)
