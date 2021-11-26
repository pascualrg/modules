# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import _
#from odoo.exceptions import ValidationError, Warning
#import secrets
import logging
from datetime import datetime, timedelta
#import re
#from odoo.exceptions import ValidationError
#from odoo import http

_logger = logging.getLogger(__name__)

class player(models.Model):
    _name = 'juego.player'
    _description = 'juego.player'

    username = fields.Char(required=True)
    name = fields.Char(required=True)
    password = fields.Char(Required=True)
    avatar = fields.Image(max_width=200, max_height=200)
    birth_year = fields.Integer()
    register_date = fields.Datetime()
    level = fields.Integer(readonly=True)
   
    npcs = fields.One2many('juego.npc', 'player')
    bunker = fields.Many2one('juego.bunker', ondelete='restrict')

    _sql_constraints = [ ('username_uniq','unique(username)','The username is in use, choose another.') ]


class npc(models.Model):
    _name = 'juego.npc'
    _description = 'juego.npc'

    name = fields.Char()
    avatar = fields.Image()
    hunger = fields.Float()
    thirst = fields.Float()
    bottle_caps = fields.Integer()
    player = fields.Many2one(string='Boss', comodel_name='juego.player', ondelete='set null')
    bunker = fields.Many2one('juego.bunker', ondelete='restrict')

    def _get_caps(self):
        return self.bottle_caps



class bunker(models.Model):
    _name = 'juego.bunker'
    _description = 'juego.bunker'

    name = fields.Char(required=True)
    bImage = fields.Image()
    water = fields.Float(default=50)
    food = fields.Float(default=60)
    bottle_caps = fields.Integer(compute='_get_caps')#compute='_get_caps'
    population = fields.Integer(compute='_get_population')
    watter_deposits = fields.Integer(default=2)
    food_pantries = fields.Integer(default=1)
    max_population = fields.Integer(default=10) #Luego con mejoras, la poblacón se podrá aumentar

    npcs = fields.One2many('juego.npc', 'bunker')
    players = fields.One2many('juego.player', 'bunker')

    _sql_constraints = [ ('name_unic','unique(name)','This bunkers name is already created') ]


    @api.depends('npcs', 'players')
    def _get_population(self):
        for b in self:
            b.population = len(b.npcs) + len(b.players)
    
    @api.depends('npcs', 'players')
    def _get_caps(self):
        for b in self:
            for npc in b.npcs:
               b.bottle_caps += npc._get_caps()
                

