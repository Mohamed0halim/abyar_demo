# -*- coding: utf-8 -*-

from odoo import (
    models,
    api,
    fields,
)


class Setting(models.TransientModel):
    _inherit = 'res.config.settings'

    done_without_approval = fields.Selection([
        ('yes', "Skip Approval Stage"),
        ('no', "Confirm all after approval"),
    ], string="Purchase Automate Setting", default='no')

    def set_values(self):
        res = super(Setting, self).set_values()
        self.env['ir.config_parameter'].set_param('purchase_automation.done_without_approval',
                                                  self.done_without_approval)
        return res

    @api.model
    def get_values(self):
        res = super(Setting, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        done_without_approval = icp_sudo.get_param('purchase_automation.done_without_approval')
        res.update(
            done_without_approval=done_without_approval
        )
        return res
