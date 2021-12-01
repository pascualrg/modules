# -*- coding: utf-8 -*-
# from odoo import http


# class TestExamen(http.Controller):
#     @http.route('/test_examen/test_examen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_examen/test_examen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_examen.listing', {
#             'root': '/test_examen/test_examen',
#             'objects': http.request.env['test_examen.test_examen'].search([]),
#         })

#     @http.route('/test_examen/test_examen/objects/<model("test_examen.test_examen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_examen.object', {
#             'object': obj
#         })
