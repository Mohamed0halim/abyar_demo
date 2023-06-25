# -*- coding: utf-8 -*-
# from odoo import http


# class IqUserJournals(http.Controller):
#     @http.route('/iq_user_journals/iq_user_journals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iq_user_journals/iq_user_journals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('iq_user_journals.listing', {
#             'root': '/iq_user_journals/iq_user_journals',
#             'objects': http.request.env['iq_user_journals.iq_user_journals'].search([]),
#         })

#     @http.route('/iq_user_journals/iq_user_journals/objects/<model("iq_user_journals.iq_user_journals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iq_user_journals.object', {
#             'object': obj
#         })
