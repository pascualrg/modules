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

class npc(models.Model):
    _name = 'juego.npc'
    _description = 'juego.npc'

    name = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200,)
    hunger = fields.Float()
    thirst = fields.Float()
    bottle_caps = fields.Integer()
    player = fields.Many2one(string='Boss', comodel_name='res.partner', ondelete='set null')
    bunker = fields.Many2one('juego.bunker', related='player.bunker', ondelete='restrict')
    level = fields.Integer()
    lugar = fields.Selection([('1','Wasteland'),('2', 'Bunker'), ('3', 'Wasteland-Searching')],default='1')
    wastelandsearchs = fields.One2many('juego.wastelandsearch', 'npc')

    search_progress = fields.Float()


    def _get_caps(self):
        return self.bottle_caps

    def leave_bunker_npc(self):
        self.write({'bunker': [(5, 0, 0)]})#'elimino' o 'limpio' el campo bunker del npc
        self.write({'player': [(5, 0, 0)]})#Abandona el jugador
        self.lugar = '1'

    def _get_search_progress(self):

        ws_num =  self.env['juego.wastelandsearch'].search_count([])

        #all_npc_wastelandsearch = self.env['juego.wastelandsearch'].search([]).filtered(lambda ws: ws.npc.id == self.id)

        search_progress = self.env['juego.wastelandsearch'].get_progress()

    def update_wastelandsearch(self):
        #get_progress()
        wastelandsearch_started = self.env['juego.wastelandsearch'].search([('state', '=', 'started')])
        for ws in wastelandsearch_started:
            ws.npc.search_progress = ws.progress
            if ws.progress >= 100:
                ws.npc.search_progress = 0
                ws.state = 'finished'
                ws.npc.lugar = '2'

    def start_searching(self):
        print("incio viaje")

        self.update_wastelandsearch()

        self.lugar="3"

        numRand = random.randint(0,1000)
        name = self.name+"_s_"+str(numRand)
        start = datetime.now()
        minutes = random.randint(5,60)
        finish = start + timedelta(minutes=minutes)
        
        vals = {'name': name, 'start':start, 'minutes':minutes, 'finish':finish, 'npc':self.id}

        self.env['juego.wastelandsearch'].create_searching(vals)

    