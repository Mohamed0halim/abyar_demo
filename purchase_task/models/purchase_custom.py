# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.exceptions import AccessError, UserError, ValidationError
from itertools import groupby
from odoo.tools import float_is_zero, format_amount, format_date, html_keep_url, is_html_empty
from odoo.fields import Command
from odoo.tools.sql import create_index
from odoo.addons.payment import utils as payment_utils
import time


class BillVendors(models.Model):
    _name = "bill.vendors"
    _description = "bill.vendors"
    _order = "vendor_name"


    vendor_name = fields.Many2one('res.partner', "Vendor Name", required=True)
    # price = fields.Char('price', required=True)
    price = fields.Float('price', required=True)
    product_qty = fields.Char('Product Qty', invisible=True, default='1')
    product_id = fields.Many2one('product.product', 'Product', required=True, domain="[('detailed_type', '=', 'service')]")
    vendor_id = fields.Many2one('purchase.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    currency = fields.Many2one('res.currency', string="Currency", ondelete='cascade')


class PurchaseOrderLines(models.Model):
    _inherit = 'purchase.order.line'

    # unit_cost = fields.Char('Unit Cost')
    unit_cost = fields.Float('Unit Cost')
    # total_cost = fields.Char('Total Cost')
    total_cost = fields.Float('Total Cost')

    # @api.onchange('unit_cost')
    # def _onchange_unit_cost(self):
    #     print('_onchange_unit_cost')
    #     for rec in self:
    #         if rec.


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_line = fields.One2many('bill.vendors', 'vendor_id', string='Vendors Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    def create_bill_vendor_driver_from_Purchase(self):
        for rec in self:
            if rec.vendor_line:
                for l in rec.vendor_line:
                    requisition_line_obj = []
                    requisition_line_obj.append((0, 0,
                                                 {'product_id': l.product_id.id,
                                                  'name': l.product_id.name,
                                                  'quantity': l.product_qty,
                                                  'price_unit': l.price,
                                                  })
                                                )
                    self.ensure_one()
                    invoice_vals = {
                        'move_type': 'in_invoice',
                        'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
                        'partner_id': l.vendor_name.id,
                        'invoice_date': fields.date.today(),
                        'invoice_payment_term_id': rec.payment_term_id.id,
                        'company_id': rec.company_id.id,
                        'state': 'draft',
                        'currency_id': l.currency.id,
                        'invoice_line_ids': requisition_line_obj,
                    }
                    # requisition_obj = self.env['account.move']
                    _prepare_invoice_line_obj = self.env['account.move.line']
                    # res = self._prepare_sbill_svendor_sname()
                    request = self.env['account.move'].create(invoice_vals)
                    # print('request', request)
                    if request:
                        request.action_post()

    # def _prepare_bill_vendor_name(self):
    #     """Prepare the dict of values to create the new invoice for a purchase order.
    #     """
    #     # self.ensure_one()
    #     # move_type = self._context.get('default_move_type', 'in_invoice')
    #     #
    #     # partner_invoice = self.env['res.partner'].browse(self.partner_id.address_get(['invoice'])['invoice'])
    #     # partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(
    #     #     ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
    #
    #     invoice_vals = {
    #         # 'move_type': move_type,
    #         # 'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
    #         # 'partner_id': self.vendor_line[0].vendor_name.id,
    #         # 'invoice_date': fields.date.today(),
    #         # 'invoice_payment_term_id': self.payment_term_id.id,
    #         # 'company_id': self.company_id.id,
    #         # 'state': 'draft',
    #         # 'invoice_line_ids': self._prepare_line_bill_vendor_name()
    #     }
    #     return invoice_vals

    # def _prepare_line_bill_vendor_name(self):
    #     requisition_line_obj = []
    #     requisition_line_obj.append((0, 0,
    #                                  {'product_id': self.vendor_line[0].product_id.id,
    #                                   'name': self.vendor_line[0].product_id.name,
    #                                   'quantity': self.vendor_line[0].product_qty,
    #                                   'price_unit': self.vendor_line[0].price,
    #                                   })
    #                                 )
    #     return requisition_line_obj

    # def create_bill_vendor_driver_name(self):
        # requisition_obj = self.env['account.move']
        # _prepare_invoice_line_obj = self.env['account.move.line']
        # res = self._prepare_bill_vendor_name()
        # request = requisition_obj.create(res).action_post()

    def button_confirm(self):
        # self.create_bill_vendor_driver_name()
        self.create_bill_vendor_driver_from_Purchase()
        super().button_confirm()
        # print('after confirm')
        for rec in self:
            if rec.order_line:
                for l in rec.order_line:
                    if l.unit_cost >= 0:
                        l.product_id.standard_price = l.unit_cost


    @api.onchange('vendor_line', 'order_line')
    def _onchange_vendor_line(self):
        # print('_onchange_vendor_line')
        for rec in self:
            total_qty = 0
            total_price = 0
            if rec.vendor_line:
                for v in rec.vendor_line:
                    if v.price:
                        if v.price > 0:
                            if v.currency.id:
                                if v.currency.id == rec.currency_id.id:
                                    total_price += v.price
                                else:
                                    # print('====', self.env.ref('base.main_company').currency_id.id)
                                    if v.currency.id == self.env.ref('base.main_company').currency_id.id:
                                        total_price += v.price
                                    else:
                                        if v.currency.rate_ids:
                                            # for r in v.currency.rate_ids:
                                            net_price = v.price / v.currency.rate_ids[0].company_rate
                                            total_price += net_price
                            else:
                                total_price += v.price
            if rec.order_line:
                for l in rec.order_line:
                    if l.product_qty:
                        total_qty += l.product_qty
            if total_qty > 0:
                cost = total_price / total_qty
            else:
                cost = 0
            # rec.order_line.unit_cost = cost
            # print('total_qty', total_qty, total_price, )
            for p in rec.order_line:
                p.unit_cost  = cost + p.price_unit
                p.total_cost  = float(p.unit_cost) * p.product_qty
