# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    # invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,
    #                            states={'draft': [('readonly', False)]}, default=fields.date.today() )


    the_beneficiary = fields.Many2one('res.partner', readonly=True, tracking=True,
        states={'draft': [('readonly', False)]}, check_company=True, string='The Beneficiary', change_default=True, )

    custom_product_id = fields.Many2one('product.product', string='Product Name', tracking=True, )
    num_of_cars = fields.Float(required=False)
    custom_select = fields.Selection(string="Type", selection=[('buy', 'Buy'), ('clearance', 'Clearance'), ],
                                     required=False, default="buy",)

    is_clearance = fields.Boolean()

    # compute = '_compute_is_clearance'
    # @api.depends('custom_select')
    # def _compute_is_clearance(self):
    #     for rec in self:
    #         rec.is_clearance = False
    #         if rec.custom_select:
    #             print('onchange_custom_select', self.env.user.lang)
    #             print('onchange_custom_select', self.with_context(lang='ar_001').partner_id)
    #             if rec.custom_select == 'clearance' and self.env.user.lang == 'ar_001' or self.env.user.lang == 'ar_SY':
    #                 # print('=======', self.env.user.lang)
    #                 rec.is_clearance = True
    #                 # self.with_context(lang='ar_001').partner_id = "اسم المخلص"

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    # _sql_constraints = [
    #     ('uniq_name', 'unique(name)',
    #      'partners should be unique for each name. '
    #      'Please check again!.'),
    # ]

    @api.onchange('name')
    @api.constrains('name')
    def _check_exist_name(self):
        for rec in self:
          if rec.name:
            all_names = []
            the_partners = self.env['res.partner'].sudo().search([('name', '=', rec.name), ('id', '!=', rec._origin.id)])
            for ss in the_partners:
              all_names.append(ss.name)
            if rec.name in all_names:
              raise ValidationError(_("partners name should be unique for each one, "
                                      "this name is already created. Please check again!."))


class ProductProductInherit(models.Model):
  _inherit = 'product.product'


  @api.onchange('name')
  @api.constrains('name')
  def _check_exist_name(self):
    for rec in self:
      if rec.name:
        all_names = []
        the_products = self.env['product.product'].sudo().search([('name', '=', rec.name), ('id', '!=', rec._origin.id)])
        for ss in the_products:
          all_names.append(ss.name)
        if rec.name in all_names:
          raise ValidationError(_("products name should be unique for each one, "
                                  "this name is already created. Please check again!."))


class ProductTemplateInherit(models.Model):
  _inherit = 'product.template'


  @api.onchange('name')
  @api.constrains('name')
  def _check_exist_name(self):
    for rec in self:
      if rec.name:
        all_names = []
        the_products = self.env['product.template'].sudo().search([('name', '=', rec.name), ('id', '!=', rec._origin.id)])
        for ss in the_products:
          all_names.append(ss.name)
        if rec.name in all_names:
          raise ValidationError(_("products name should be unique for each one, "
                                  "this name is already created. Please check again!."))
