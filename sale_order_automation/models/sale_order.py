from odoo import api, fields, models, exceptions


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:

            warehouse = order.warehouse_id
            if warehouse.is_delivery_set_to_done and order.picking_ids: 
                for picking in self.picking_ids:
                    picking.action_assign()
                    picking.action_set_quantities_to_reservation()
                    picking.action_confirm()
                    picking.button_validate()

            if warehouse.create_invoice and not order.invoice_ids:
                order._create_invoices()
            if warehouse.validate_invoice and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_post()

        return res  
