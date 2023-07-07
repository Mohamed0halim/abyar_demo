# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from collections import Counter
from collections import defaultdict

class JournalItemsWizard(models.TransientModel):
    _name = "vendor.wizard"


    start_date = fields.Date('Start Period', required=True, readonly=False)
    end_date = fields.Date('End Period', required=True, readonly=False)
    the_partner_id = fields.Many2one('res.partner', required=True, readonly=False, tracking=True, string='The partner')

    def to_add_commas(self, number):
        number = str(number)
        result = ""
        length = len(number)
        for i in range(length):
            if i > 0 and (length - i) % 3 == 0:
                result += ","
            result += number[i]
        return result

        # To remove any number after the dot (decimal point) in a string if the number is less than zero or equal to zero,
        # you can modify the previous code as follows:"

    def remove_decimal(self, number):
        parts = str(number).split(".")
        result = parts[0] if len(parts) > 0 else ""
        if len(parts) > 1:
            decimal_part = parts[1]
            if int(decimal_part) <= 0:
                return result
        return str(number)

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

    def sum_duplicates(list_of_dicts, key_fields):
        summed_dict = {}
        for dictionary in list_of_dicts:
            compound_key = tuple(dictionary[field] for field in key_fields)
            value = float(dictionary['total_fees'])  # Convert 'total_fees' to float
            value2 = float(dictionary['total_receipts'])  # Convert 'total_fees' to float
            if compound_key in summed_dict:
                summed_dict[compound_key] += value
                summed_dict[compound_key] += value2
            else:
                summed_dict[compound_key] = value
                summed_dict[compound_key] = value2

        return summed_dict


    def get_general_vendor_bill_report(self):
        domain = []
        list_data = []
        lines_data = []
        name_of_bill = ''
        last_balance = 0.0
        if self.env.context.get('active_id'):
            current_record1 = self.env['account.move'].search([('id', '=', self.env.context.get('active_id'))])
            if current_record1:
                # if current_record1.move_type == 'out_invoice':
                last_inv_for_same_partner = self.env['account.move'].search(
                    [('id', '!=', self.env.context.get('active_id')),
                     ('partner_id.id', '=', current_record1.partner_id.id),
                     ('move_type', '=', 'in_invoice')
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
                    # last_balance = last_inv_for_same_partner.final_customer_balance
                    last_balance = current_record1.last_customer_balance_from_last_inv
                    if last_balance < 0:
                        last_balance = last_balance * -1
                frac = last_balance - int(last_balance)
                if frac < 0.5:
                    last_balance = int(last_balance)
                else:
                    last_balance = last_balance
                # last_balance = float(last_balance)

                # create_date
                # current_record = self.env['account.move'].browse(self.env.context.get('active_id'))
                # print('current_record1==', current_record1)
                # print('invoice_line_ids==', current_record1.invoice_line_ids)
                # print(format(last_balance,","))
                # total_fees_quant = 0
                total_fees_and_receipts_quant = 0.0
                for l in current_record1.invoice_line_ids:
                    total_receipts = 0.0
                    total_fees = 0.0
                    # # print('currency_id=', account.currency_id.name)
                    # # print('tax_totals_json', account.tax_totals_json)
                    # # print('invoice_payments_widget', account.invoice_payments_widget)
                    # custom_date = account.invoice_date
                    # name_of_product = account.custom_product_id.name
                    # num_of_cars = account.num_of_cars
                    # # print('amount_residual', account.amount_residual)
                    # if account.invoice_line_ids:
                    #     for l in account.invoice_line_ids:
                    if l.fees_or_receipts == 'receipts':
                        # total_receipts = l.price_unit
                        total_receipts = l.price_subtotal
                        # total_receipts_quant += l.quantity
                    if l.fees_or_receipts == 'fees':
                        total_fees = l.price_subtotal
                        # total_fees_quant += l.quantity
                    # total_fees_and_receipts_quant += l.quantity
                    total_fees_and_receipts_quant = l.price_subtotal

                    print('===', l.product_id)
                    valss1 = {
                        'date': current_record1.invoice_date,
                        'custom_date': l.custom_date,
                        'total_receipts': total_receipts,
                        'total_fees': total_fees,
                        'pro_id': l.product_id.id,
                        'product_id': l.product_id.name,
                        'custom_notes': l.custom_notes,
                        'how_many_cars': l.how_many_cars,
                        # 'quant': l.quantity,
                        # 'price': l.price_unit,
                        # 'price_subtotal': l.price_subtotal,
                        'total_fees_and_receipts_quant': total_fees_and_receipts_quant,
                    }
                    lines_data.append(valss1)
                    name_of_bill = current_record1.name_of_bill
        last_balance3 = format(last_balance, ",")

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
        total_for_amount = 0.0
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
        last_balance2 = last_balance
        last_balance = self.remove_decimal(last_balance)
        # print('lines_data==', lines_data)
        # print('/'*20)
        result = defaultdict(lambda: defaultdict(int))
        # for item in lines_data:
        for item in reversed(lines_data):
            key = (item['pro_id'], item['custom_date'])
            result[key]['total_fees'] += item['total_fees']
            result[key]['total_receipts'] += item['total_receipts']
            result[key]['how_many_cars'] = item['how_many_cars']
            result[key]['product_id'] = item['product_id']

        result_list = [
            {'pro_id': key[0], 'custom_date': key[1], 'how_many_cars': result[key], 'product_id': result[key], **values}
            for key, values in result.items()
        ]
        # print('result_list==', result_list)
        data = {
            # 'invoice_lines': lines_data,
            # 'invoice_lines': filtered_data,
            'invoice_lines': result_list,
            'move_lines': list_data,
            'from': self.start_date,
            'to': self.end_date,
            'partner': self.the_partner_id.name,
            'name_of_bill': name_of_bill,
            # 'last_balance': self.to_add_commas(last_balance),
            'last_balance': last_balance3,
            'last_balance2': last_balance2,
        }
        # print('list_data==', list_data)
        return self.env.ref('ageneral_weekly_account_statement_for_the_vendor.general_report_for_vendor_action').report_action(self, data=data)
