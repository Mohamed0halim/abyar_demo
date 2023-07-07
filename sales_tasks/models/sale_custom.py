# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class SalesBillVendors(models.Model):
    _name = "sbill.svendors"
    _description = "sbill.svendors"
    _order = "svendor_name"

    svendor_name = fields.Many2one('res.partner', "Vendor Name", required=True)
    sprice = fields.Float('price', required=True)
    sproduct_qty = fields.Char('Product Qty', invisible=True, default='1')
    sproduct_id = fields.Many2one('product.product', 'Product', required=True, domain="[('detailed_type', '=', 'service')]")
    svendor_id = fields.Many2one('sale.order', string='Order Reference', index=True, required=False, ondelete='cascade')
    acc_svendor_id = fields.Many2one('account.move', string='Order Reference', index=True, required=False, ondelete='cascade')
    s_currency = fields.Many2one('res.currency', string="Currency", ondelete='cascade')


    is_invoiced = fields.Boolean()

# class PurchaseOrderLines(models.Model):
#     _inherit = 'purchase.order.line'
#
#     # unit_cost = fields.Char('Unit Cost')
#     unit_cost = fields.Float('Unit Cost')
#     # total_cost = fields.Char('Total Cost')
#     total_cost = fields.Float('Total Cost')
#
#     # @api.onchange('unit_cost')
#     # def _onchange_unit_cost(self):
#     #     print('_onchange_unit_cost')
#     #     for rec in self:
#     #         if rec.


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    vendor_line = fields.One2many('sbill.svendors', 'svendor_id', string='Vendors Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    # def _prepare_sbill_svendor_sname(self):
    #     """Prepare the dict of values to create the new invoice for a purchase order.
    #     """
    #     self.ensure_one()
    #     move_type = self._context.get('default_move_type', 'in_invoice')
    #     # partner_invoice = self.env['res.partner'].browse(self.partner_id.address_get(['invoice'])['invoice'])
    #     # partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(
    #     #     ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
    #     invoice_vals = {
    #         'move_type': move_type,
    #         'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
    #         'partner_id': self.vendor_line[0].svendor_name.id,
    #         'invoice_date': fields.date.today(),
    #         'invoice_payment_term_id': self.payment_term_id.id,
    #         'company_id': self.company_id.id,
    #         'state': 'draft',
    #         'invoice_line_ids': self._prepare_sline_sbill_svendor_name()
    #     }
    #     return invoice_vals

    # def _prepare_sline_sbill_svendor_name(self):
    #     requisition_line_obj = []
    #     requisition_line_obj.append((0, 0,
    #                                  {'product_id': self.product_id.id,
    #                                   'name': self.product_id.name,
    #                                   'quantity': self.vendor_line[0].product_qty,
    #                                   'price_unit': self.vendor_line[0].price,
    #                                   })
    #                                 )
    #     return requisition_line_obj

    def create_sbill_svendor_sdriver_name(self):
        for rec in self:
            if rec.vendor_line:
                for l in rec.vendor_line:
                    requisition_line_obj = []
                    requisition_line_obj.append((0, 0,
                                                 {'product_id': l.sproduct_id.id,
                                                  'name': l.sproduct_id.name,
                                                  'quantity': l.sproduct_qty,
                                                  'price_unit': l.sprice,
                                                  })
                                                )
                    self.ensure_one()
                    move_type = self._context.get('default_move_type', 'in_invoice')
                    # partner_invoice = self.env['res.partner'].browse(self.partner_id.address_get(['invoice'])['invoice'])
                    # partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(
                    #     ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
                    invoice_vals = {
                        'move_type': move_type,
                        'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
                        'partner_id': l.svendor_name.id,
                        'invoice_date': fields.date.today(),
                        'invoice_payment_term_id': rec.payment_term_id.id,
                        'currency_id': l.s_currency.id,
                        # 'company_id': rec.company_id.id,
                        'state': 'draft',
                        'invoice_line_ids': requisition_line_obj,
                    }
                    # requisition_obj = self.env['account.move']
                    _prepare_invoice_line_obj = self.env['account.move.line']
                    # res = self._prepare_sbill_svendor_sname()
                    request = self.env['account.move'].create(invoice_vals)
                    print('request', request)
                    if request:
                        request.action_post()

    def action_confirm(self):
        self.create_sbill_svendor_sdriver_name()
        super().action_confirm()
        # print('after confirm')
        # for rec in self:
        #     if rec.order_line:
        #         for l in rec.order_line:
        #             if l.unit_cost >= 0:
        #                 l.product_id.standard_price = l.unit_cost



    # @api.onchange('vendor_line', 'order_line')
    # def _onchange_vendor_line(self):
    #     # print('_onchange_vendor_line')
    #     for rec in self:
    #         total_qty = 0
    #         total_price = 0
    #         if rec.vendor_line:
    #             for v in rec.vendor_line:
    #                 if v.price:
    #                     if v.price > 0:
    #                         total_price += v.price
    #         if rec.order_line:
    #             for l in rec.order_line:
    #                 if l.product_qty:
    #                     total_qty += l.product_qty
    #         if total_qty > 0:
    #             cost = total_price / total_qty
    #         else:
    #             cost = 0
    #         # # rec.order_line.unit_cost = cost
    #         # # print('total_qty', total_qty, total_price, )
    #         # for p in rec.order_line:
    #         #     p.unit_cost  = cost + p.price_unit
    #         #     p.total_cost  = float(p.unit_cost) * p.product_qty

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).', self.company_id.name, self.company_id.id))

        line_obj = []
        for rec in self:
            if rec.vendor_line:
                for l in rec.vendor_line:
                    line_obj.append((0, 0,{
                        'sproduct_id': l.sproduct_id.id,
                        'svendor_name': l.svendor_name.id,
                        'sprice': l.sprice,
                        # 'svendor_id': rec,
                    }))
        # print('line_obj', line_obj)

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids.filtered(lambda bank: bank.company_id.id in (self.company_id.id, False))[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'acc_vendor_line': line_obj,

        }
        # print('invoice_vals', invoice_vals)
        return invoice_vals
