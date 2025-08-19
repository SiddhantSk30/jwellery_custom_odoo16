from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class CustomerPricingPortal(http.Controller):
    @http.route('/my/pricing', type='http', auth="user", website=True)
    def portal_my_pricing(self, **kw):
        try:
            user = request.env.user
            _logger.info("Portal user access attempt: %s (ID: %s)", user.name, user.id)
            
            if not user.has_group('base.group_portal'):
                _logger.warning("Non-portal user attempted access")
                return request.redirect('/my/home?error=access')
            
            commercial_partner = user.partner_id.commercial_partner_id
            _logger.info("Commercial partner: %s (ID: %s)", commercial_partner.name, commercial_partner.id)
            
            # Use sudo with explicit domain to ensure access
            quotations = request.env['sale.order'].sudo().search([
                ('partner_id', 'child_of', commercial_partner.id),
                ('state', 'in', ['draft', 'sent', 'sale'])
            ])
            
            _logger.info("Found %d quotations for user", len(quotations))
            
            return request.render('customer_pricing.portal_my_pricing', {
                'quotations': quotations,
                'page_name': 'pricing',
            })
        except Exception as e:
            _logger.error("Portal pricing error: %s", str(e), exc_info=True)
            return request.redirect('/my/home?error=access')

    @http.route('/my/orders/view/<int:order_id>', type='http', auth="user", website=True)
    def custom_order_detail(self, order_id, **kw):
        try:
            user = request.env.user
            _logger.info("Order view attempt for order ID: %s by user %s", order_id, user.name)
            
            order = request.env['sale.order'].sudo().browse(order_id)
            
            if not order.exists():
                _logger.warning("Order not found: %s", order_id)
                return request.redirect('/my/pricing?error=notfound')
            
            if order.partner_id.commercial_partner_id != user.partner_id.commercial_partner_id:
                _logger.warning("Access denied for order %s (user: %s)", order_id, user.name)
                return request.redirect('/my/pricing?error=access')
            
            order_data = order.read([
                'name', 'date_order', 'partner_id', 'state',
                'currency_id', 'amount_total'
            ])[0]
            
            order_lines = []
            for line in order.order_line:
                order_lines.append({
                    'product': line.product_id.display_name,
                    'description': line.name,
                    'quantity': line.product_uom_qty,
                    'unit_price': line.price_unit,
                    'subtotal': line.price_subtotal
                })
            
            return request.render('customer_pricing.custom_quotation_detail', {
                'order': order,
                'order_data': order_data,
                'order_lines': order_lines,
                'currency': order.currency_id,
                'page_name': 'pricing',
            })
        except Exception as e:
            _logger.error("Order detail error: %s", str(e), exc_info=True)
            return request.redirect('/my/pricing?error=unknown')
        


    @http.route('/my/orders/confirm/<int:order_id>', type='http', auth="user", website=True)
    def confirm_order(self, order_id, **kw):
        try:
            user = request.env.user
            order = request.env['sale.order'].sudo().browse(order_id)

            if not order.exists():
                return request.redirect('/my/pricing?error=notfound')

            if order.partner_id.commercial_partner_id != user.partner_id.commercial_partner_id:
                return request.redirect('/my/pricing?error=access')

            if order.state in ['draft', 'sent']:
                order.action_confirm()
                return request.redirect('/my/orders/view/%d?success=confirmed' % order_id)
            else:
                return request.redirect('/my/orders/view/%d?error=invalid_state' % order_id)

        except Exception as e:
            _logger.error("Order confirmation error: %s", str(e), exc_info=True)
            return request.redirect('/my/orders/view/%d?error=unknown' % order_id)

        

    @http.route('/my/orders/cancel/<int:order_id>', type='http', auth="user", website=True)
    def cancel_order(self, order_id, **kw):
        try:
            user = request.env.user
            order = request.env['sale.order'].sudo().browse(order_id)
            
            if not order.exists():
                return request.redirect('/my/pricing?error=notfound')
                
            if order.partner_id.commercial_partner_id != user.partner_id.commercial_partner_id:
                return request.redirect('/my/pricing?error=access')
                
            if order.state in ['draft', 'sent']:
                order.action_cancel()
                return request.redirect('/my/orders/view/%d?success=cancelled' % order_id)
            else:
                return request.redirect('/my/orders/view/%d?error=invalid_state' % order_id)
                
        except Exception as e:
            _logger.error("Order cancellation error: %s", str(e), exc_info=True)
            return request.redirect('/my/orders/view/%d?error=unknown' % order_id)