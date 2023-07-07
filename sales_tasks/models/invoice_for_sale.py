# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError




class CustomAccountMoveInherit(models.Model):
  _inherit = 'account.move'

  acc_vendor_line = fields.One2many('sbill.svendors', 'acc_svendor_id', string='Vendors Lines',
                                    states={'cancel': [('readonly', True)], 'posted': [('readonly', True)]}, copy=True)

  def create_sbill_vendor_driver_from_invoice(self):
    for rec in self:
      if rec.acc_vendor_line:
        for l in rec.acc_vendor_line:
          requisition_line_obj = []
          requisition_line_obj.append((0, 0,
                                       {'product_id': l.sproduct_id.id,
                                        'name': l.sproduct_id.name,
                                        'quantity': l.sproduct_qty,
                                        'price_unit': l.sprice,
                                        })
                                      )
          self.ensure_one()
          # move_type = self._context.get('default_move_type', 'in_invoice')
          # partner_invoice = self.env['res.partner'].browse(self.partner_id.address_get(['invoice'])['invoice'])
          # partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(
          #     ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
          invoice_vals = {
            'move_type': 'in_invoice',
            'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
            'partner_id': l.svendor_name.id,
            'invoice_date': fields.date.today(),
            'invoice_payment_term_id': rec.invoice_payment_term_id.id,
            # 'company_id': rec.company_id.id,
            'state': 'draft',
            'invoice_line_ids': requisition_line_obj,
          }
          # requisition_obj = self.env['account.move']
          _prepare_invoice_line_obj = self.env['account.move.line']
          # res = self._prepare_sbill_svendor_sname()
          request = self.env['account.move'].create(invoice_vals)
          # print('request', request)
          if request:
            request.action_post()

  def action_post(self):
    self.create_sbill_vendor_driver_from_invoice()
    super().action_post()

class AccountMoveLineInheritCustom(models.Model):
    _inherit = 'account.move.line'


    fees_or_receipts = fields.Selection(selection=[('receipts', 'Receipts'), ('fees', 'Fees')], required=False, )

# class SaleAdvancePaymentInv(models.TransientModel):
#   _inherit = "sale.advance.payment.inv"
#
#   def create_invoices(self):
#     sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
#
#     if self.advance_payment_method == 'delivered':
#       sale_orders._create_invoices(final=self.deduct_down_payments)
#     else:
#       # Create deposit product if necessary
#       if not self.product_id:
#         vals = self._prepare_deposit_product()
#         self.product_id = self.env['product.product'].create(vals)
#         self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)
#
#       sale_line_obj = self.env['sale.order.line']
#       for order in sale_orders:
#         amount, name = self._get_advance_details(order)
#
#         if self.product_id.invoice_policy != 'order':
#           raise UserError(
#             _('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
#         if self.product_id.type != 'service':
#           raise UserError(
#             _("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
#         taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
#         tax_ids = order.fiscal_position_id.map_tax(taxes).ids
#         analytic_tag_ids = []
#         for line in order.order_line:
#           analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
#
#         so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
#         so_line = sale_line_obj.create(so_line_values)
#         self._create_invoice(order, so_line, amount)
#     if self._context.get('open_invoices', False):
#       return sale_orders.action_view_invoice()
#     return {'type': 'ir.actions.act_window_close'}
#
#   # def _prepare_invoice_values(self, order, name, amount, so_line):
#   #   invoice_vals = {
#   #     'ref': order.client_order_ref,
#   #     'move_type': 'out_invoice',
#   #     'invoice_origin': order.name,
#   #     'invoice_user_id': order.user_id.id,
#   #     'narration': order.note,
#   #     'partner_id': order.partner_invoice_id.id,
#   #     'fiscal_position_id': (order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(
#   #       order.partner_id.id)).id,
#   #     'partner_shipping_id': order.partner_shipping_id.id,
#   #     'currency_id': order.pricelist_id.currency_id.id,
#   #     'payment_reference': order.reference,
#   #     'invoice_payment_term_id': order.payment_term_id.id,
#   #     'partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
#   #     'team_id': order.team_id.id,
#   #     'campaign_id': order.campaign_id.id,
#   #     'medium_id': order.medium_id.id,
#   #     'source_id': order.source_id.id,
#   #     'acc_vendor_line': order.vendor_line,
#   #     'invoice_line_ids': [(0, 0, {
#   #       'name': name,
#   #       'price_unit': amount,
#   #       'quantity': 1.0,
#   #       'driver_name': order.driver_name.id,
#   #       'product_id': self.product_id.id,
#   #       'product_uom_id': so_line.product_uom.id,
#   #       'tax_ids': [(6, 0, so_line.tax_id.ids)],
#   #       'sale_line_ids': [(6, 0, [so_line.id])],
#   #       'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
#   #       'analytic_account_id': order.analytic_account_id.id or False,
#   #     })],
#   #   }
#   #   print('invoice_vals', invoice_vals)
#   #   return invoice_vals
