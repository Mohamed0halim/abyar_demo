# -*- coding: utf-8 -*-

from odoo import models, fields, api


class iq_inherit_users(models.Model):
    _inherit = 'res.users'

    iq_defaultpjournal = fields.Many2one('account.journal' ,string='Default Journal')
    iq_journals = fields.Many2many('account.journal' ,string='Allowed Journals')

    
    
    
    
    
    
    
  
    
   
