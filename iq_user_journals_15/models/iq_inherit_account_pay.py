
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class iq_AccountMovepaymenregistertInherit(models.TransientModel):
    _inherit = 'account.payment.register'
    
    
    @api.onchange('journal_id')
    def get_domaied_journals(self):
       
                
        domain_on_types=[('id' ,'in',self.env.user.iq_journals.ids), ('type', 'in', ('bank', 'cash')),('company_id', '=', self.company_id.id)]
        
        return {'domain': {'journal_id': domain_on_types}}
    
    
    

    @api.depends('company_id', 'source_currency_id')
    def _compute_journal_id(self):
        for wizard in self:
#             domain = [
#                 ('type', 'in', ('bank', 'cash')),
#                 ('company_id', '=', wizard.company_id.id),
#             ]
#             journal = None
#             if wizard.source_currency_id:
#                 journal = self.env['account.journal'].search(domain + [('currency_id', '=', wizard.source_currency_id.id)], limit=1)
#             if not journal:
#                 journal = self.env['account.journal'].search(domain, limit=1)
#                 
#                 
#                 
#             wizard.journal_id = journal
            
            
            wizard.journal_id = self.env.user.iq_defaultpjournal
    
    
    


class iq_AccountMovepaymentInherit(models.Model):

    _inherit = 'account.payment'
    

    
    @api.model
    def default_get(self, fields):
        print("33333333333366666")
        vals = super(iq_AccountMovepaymentInherit, self).default_get(fields)

        vals['journal_id']=self.env.user.iq_defaultpjournal
        return vals
    
    
    
    @api.onchange('journal_id')
    def get_domaied_journals(self):
       
                
        domain_on_types=[('id' ,'in',self.env.user.iq_journals.ids), ('type', 'in', ('bank', 'cash')),('company_id', '=', self.company_id.id)]
        
        return {'domain': {'journal_id': domain_on_types}}
    
    
    
    
        
