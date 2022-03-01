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

class wastelandsearch(models.Model):
    _name = 'juego.wastelandsearch'
    _description = 'juego.wastelandsearch'

    name = fields.Char()
    start = fields.Datetime()
    finish = fields.Datetime()
    minutes = fields.Integer()
    jornada = fields.Integer(default=24)
    npc = fields.Many2one(comodel_name='juego.npc', ondelete='set null')

    state = fields.Selection([('started', 'Started'),('finished', 'Finished')],default='started')

    progress = fields.Float(compute='get_progress')

    @api.model
    def create_searching(self, vals):
        res = super(wastelandsearch, self).create(vals)
        return res

    @api.depends('start', 'finish')
    def get_progress(self):
        
        for ws in self:
            time_remaining = ws.finish -  datetime.now()
            time_remaining = time_remaining.total_seconds() / 60 
            ws.progress = (1 - time_remaining / ws.minutes) * 100
            ws.npc.search_progress = ws.progress
            
            if ws.progress >= 100:
                ws.progress = 100
                ws.state = 'finished'

    def update_wastelandsearch(self):
        #get_progress()
        wastelandsearch_started = self.search([('state', '=', 'started')])
        for ws in wastelandsearch_started:
            ws.npc.search_progress = ws.progress
            if ws.progress >= 100:
                ws.state = 'finished'
                chapasRandom = random.randint(50,250) #Cantidad de chapas encontradas durante la busqueda
                print("Chapas conseguidas en la busqueda: "+str(chapasRandom))
                ws.npc.bottle_caps += chapasRandom
                ws.npc.search_progress = 0
                ws.npc.lugar = '2'