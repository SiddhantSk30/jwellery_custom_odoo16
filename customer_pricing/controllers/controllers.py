# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerPricing(http.Controller):
#     @http.route('/customer_pricing/customer_pricing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_pricing/customer_pricing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_pricing.listing', {
#             'root': '/customer_pricing/customer_pricing',
#             'objects': http.request.env['customer_pricing.customer_pricing'].search([]),
#         })

#     @http.route('/customer_pricing/customer_pricing/objects/<model("customer_pricing.customer_pricing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_pricing.object', {
#             'object': obj
#         })
