# -*- coding: utf-8 -*-
# from odoo import http


# class Preexamen(http.Controller):
#     @http.route('/preexamen/preexamen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/preexamen/preexamen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('preexamen.listing', {
#             'root': '/preexamen/preexamen',
#             'objects': http.request.env['preexamen.preexamen'].search([]),
#         })

#     @http.route('/preexamen/preexamen/objects/<model("preexamen.preexamen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('preexamen.object', {
#             'object': obj
#         })
