# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def _automate_purchase_order(self):
        for purchase in self:
            if purchase.picking_ids:
                for pickingd_id in purchase.picking_ids:
                    if pickingd_id.state == 'assigned':
                        pickingd_id.action_assign()
                        pickingd_id.action_set_quantities_to_reservation()
                        pickingd_id.button_validate()
            if not purchase.invoice_ids:
                purchase.action_create_invoice()
            if purchase.invoice_ids:
                for invoice in purchase.invoice_ids:
                    invoice.action_post()


    def button_approve(self, force=False):
        parent_result = super(PurchaseOrder, self).button_approve(force=force)
        self._create_picking()
        self._automate_purchase_order()
        return parent_result


    def _approval_allowed(self):
        parent_result = super(PurchaseOrder, self)._approval_allowed()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        result = icp_sudo.get_param('purchase_automation.done_without_approval')
        done_without_approval = True if result == 'yes' else False
        if done_without_approval:
            return True
        return parent_result


    def _prepare_invoice(self):
        parent_result = super(PurchaseOrder,self)._prepare_invoice()
        parent_result.update(invoice_date=fields.Date.today())
        return parent_result

