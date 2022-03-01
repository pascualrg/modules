from odoo import models, fields, api
from odoo import _
import random
#from odoo.exceptions import ValidationError, Warning
#import secrets
import logging
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo import http
import base64
import re


from odoo.tools import image

class explorer_pass(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    explicacion = fields.Char(default="Pase explorador.", readonly="True")
    have_explorer_pass = fields.Boolean(default=False)
    

class sale_explorer_pass(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    explorer_purchased = fields.Boolean(default=False)

    def buy_explorer_pass(self):

        premium_products = self.order_line.filtered(lambda p: p.product_id.have_explorer_pass == True and self.explorer_purchased == False)
        for p in premium_products:
            self.partner_id.buy_explorer_pass()

    def write(self,values):
        super(sale_explorer_pass,self).write(values)
        self.buy_explorer_pass()

    @api.model
    def create(self,values):
        record = super(sale_explorer_pass,self).create(values)
        record.buy_explorer_pass()
        return record