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

    username = fields.Char(Required=True)
    name = fields.Char(Required=True)
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
    hunger = fields.Float()
    thirst = fields.Float()
    bottle_caps = fields.Integer()

    player = fields.Many2one('juego.player', ondelete='set null')
    bunker = fields.Many2one('juego.bunker', ondelete='restrict')



class bunker(models.Model):
    _name = 'juego.bunker'
    _description = 'juego.bunker'

    name = fields.Char()

    population = fields.Integer(compute='_get_population')
    max_population = fields.Integer(default=10) #Luego con mejoras, la poblacón se podrá aumentar

    npcs = fields.One2many('juego.npc', 'bunker')
    players = fields.One2many('juego.player', 'bunker')

    @api.depends('npcs', 'players')
    def _get_population(self):
        for b in self:
            b.population = len(b.npcs) + len(b.players)

# class juego(models.Model):
#     _name = 'juego.juego'
#     _description = 'juego.juego'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
