from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
class DeliveryOrderReportWizard(models.TransientModel):
    _name = 'delivery.order.report'
    _description = 'Delivery Order Report Wizard'

    filter= fields.Selection([('all','All'),('gold', 'Gold'), ('silver', 'Silver')],
                                    string='Filter')
    report_type = fields.Selection([
        ('receipts', 'Receipts'),
        ('internal_transfers', 'Internal Transfers'),
        ('delivery_orders', 'Delivery Orders')
    ], string='Report Type', required=True)
    location_id = fields.Many2one('stock.location', string='Select Location')
    date_from = fields.Date('From Date', required= True)
    date_to = fields.Date('To Date', required=True)
    
    def get_from_date(self):
        return self.date_from
    
    def get_to_date(self):
        return self.date_to
    
    def get_metal_type(self):
        return self.filter.capitalize()
    def get_report_name(self):
        if self.report_type == "receipts":
            return "Receipts"
        elif self.report_type == "internal_transfers":
            return "Internal Transfers"   
        elif self.report_type == "delivery_orders":
            return "Delivery Orders"
  
    # Define a function to print delivery orders
    def print_delivery_orders(self):
       
        return self.env.ref(
            "dw_delivery_orders_report.action_report_delivery_order"
        ).report_action(self)

    def generate_data(self):
        """Generate data to be printed in the report"""
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValidationError(
                    ("from date should be less than To date")
                )
        if self.report_type == 'delivery_orders':    
            if self.filter == 'all':    
                products_data = []
                product = self.env['product.template'].search([])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'outgoing'), ('state','=','done'),('location_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = round(prod.gross_wt, 2) 
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,
                                })
                        
                print("********",products_data) 
                return products_data
            if self.filter == 'gold':    
                products_data = []
                product = self.env['product.template'].search([('metal', '=', 'gold')])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'outgoing'), ('state','=','done'),('location_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = prod.gross_wt
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,
                                
                                })
                        
                print("********",products_data) 
                return products_data    
            if self.filter == 'silver':    
                products_data = []
                product = self.env['product.template'].search([('metal', '=', 'silver')])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'outgoing'), ('state','=','done'),('location_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = prod.gross_wt
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,                               
                                })
                        
                print("********",products_data) 
                return products_data

        elif self.report_type == 'receipts':    
            if self.filter == 'all':    
                products_data = []
                product = self.env['product.template'].search([])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done'),('location_dest_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = round(prod.gross_wt, 2) 
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,
                                })
                        
                print("********",products_data) 
                return products_data
            if self.filter == 'gold':    
                products_data = []
                product = self.env['product.template'].search([('metal', '=', 'gold')])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done'),('location_dest_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = prod.gross_wt
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,
                                
                                })
                        
                print("********",products_data) 
                return products_data    
            if self.filter == 'silver':    
                products_data = []
                product = self.env['product.template'].search([('metal', '=', 'silver')])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done'),('location_dest_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = prod.gross_wt
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,                               
                                })
                        
                print("********",products_data) 
                return products_data
        elif self.report_type == 'internal_transfers':    
            if self.filter == 'all':    
                products_data = []
                product = self.env['product.template'].search([])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'internal'), ('state','=','done'),('location_dest_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = round(prod.gross_wt, 2) 
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,
                                })
                        
                print("********",products_data) 
                return products_data
            if self.filter == 'gold':    
                products_data = []
                product = self.env['product.template'].search([('metal', '=', 'gold')])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'internal'), ('state','=','done'),('location_dest_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = prod.gross_wt
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,
                                
                                })
                        
                print("********",products_data) 
                return products_data    
            if self.filter == 'silver':    
                products_data = []
                product = self.env['product.template'].search([('metal', '=', 'silver')])
                for prod in product:
                    ttl_de_qty = cost_price=0 
                    prod_name = ''
                    product_code = None
                    delivery_orders = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'internal'), ('state','=','done'),('location_dest_id','=',self.location_id.id)])
                    for rec in delivery_orders:
                        for move_line in rec.move_line_ids:
                            if prod.code == move_line.product_id.pro_code:
                                product_code = move_line.product_id.pro_code
                                prod_name = move_line.product_id.name
                                ttl_de_qty = ttl_de_qty + move_line.qty_done
                    if prod_name: 

                        qty = prod.qty_available + ttl_de_qty
                        gw = prod.gross_wt
                        ttl_on_hand = qty - ttl_de_qty
                        cost_price = round(prod.standard_price, 2)  
                        ttl_de_gw =  round((ttl_de_qty*gw), 2)  
                        on_hand =  abs(round((ttl_on_hand * gw), 2))  
                        # receipt_gw = abs(round((ttl_de_qty * gw), 2))
                        ttl_de_cp = round((ttl_de_qty * cost_price), 2)
                        ttl_onhand_cp = abs(round((ttl_on_hand * cost_price), 2))
                        receipts = self.env['stock.picking'].search([('scheduled_date', '>=', self.date_from), ('scheduled_date', '<=', self.date_to), ('picking_type_id.code', '=', 'incoming'), ('state','=','done')])
                        receipt_gw = 0.0
                        for rec in  receipts:
                            for line in rec.move_ids_without_package:
                                if product_code == line.product_id.pro_code:
                                    receipt_gw += line.quantity_done
                        ttl_receipt_gw = abs(round((receipt_gw * gw), 2)) 
                        products_data.append({
                                    'product_name': prod_name,
                                    'qty': qty,
                                    'gw': gw,
                                    'ttl_receipts':receipt_gw,
                                    'ttl_on_hand':ttl_on_hand,
                                    'ttl_de_gw':ttl_de_gw,
                                    'on_hand' : on_hand,
                                    'receipt_gw':ttl_receipt_gw,
                                    'delivered_qty': ttl_de_qty,
                                    'cost_price':cost_price,
                                    'ttl_de_cp' : ttl_de_cp,
                                    'ttl_onhand_cp': ttl_onhand_cp,                               
                                })
                        
                print("********",products_data) 
                return products_data    
        else:
            raise ValidationError("Please Enter The Report Type")              
 
