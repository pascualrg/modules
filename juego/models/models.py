# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import _
import random
#from odoo.exceptions import ValidationError, Warning
#import secrets
import logging
from datetime import datetime, timedelta
#import re
from odoo.exceptions import ValidationError
from odoo import http

_logger = logging.getLogger(__name__)


class banner_juego_controller(http.Controller):
    @http.route('/juego/banner', auth='user', type='json')
    def banner(self):
        return {
            'html': """
                <div  class="juego_banner" 
                style="height: 280px; background-size:100%; background-image: url(/school/static/src/img/banner.jpg)">
                <p>BANNER</p>
                </div> """
        }


class player(models.Model):
    _name = 'juego.player'
    _description = 'juego.player'

    username = fields.Char(required=True)
    name = fields.Char(required=True)
    password = fields.Char(required=True)
    avatar = fields.Image(max_width=200, max_height=200)
    birth_year = fields.Integer(default="2003")
    register_date = fields.Datetime(default=lambda self:fields.Datetime.now(), store=True, readonly=True)
    level = fields.Integer(readonly=True)
    state = fields.Selection([('1','Wilderness'),('2', 'Bunker')],default='1')

   
    npcs = fields.One2many('juego.npc', 'player', readonly=True)
    bunker = fields.Many2one('juego.bunker', ondelete='restrict', readonly=True)

    _sql_constraints = [ ('username_uniq','unique(username)','The username is in use, choose another.') ]

    def recruit_npc(self):
            npcs = self.env['juego.npc']._get_npcs()
            #print(len(npcs))
    def find_bunker(self):
            print("Buscando bunker")
            



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
    level = fields.Integer()

    def _get_caps(self):
        return self.bottle_caps

    def _get_npcs(self):
        npcs = []
        print("DEBUG:")
        print(self.name)

        #return npcs



class bunker(models.Model):
    _name = 'juego.bunker'
    _description = 'juego.bunker'

    name = fields.Char(required=True)
    bImage = fields.Image()
    water = fields.Float(default=50)
    food = fields.Float(default=60)
    bottle_caps = fields.Integer(compute='_get_caps')#compute='_get_caps'
    population = fields.Integer(compute='_get_population')
    water_deposits = fields.Integer(default=2)
    food_pantries = fields.Integer(default=1)
    max_population = fields.Integer(default=10) #Luego con mejoras, la poblacón se podrá aumentar

    npcs = fields.One2many('juego.npc', 'bunker')
    players = fields.One2many('juego.player', 'bunker')

    _sql_constraints = [ ('name_unic','unique(name)','This bunkers name is already created') ]


    @api.depends('npcs', 'players')
    def _get_population(self):
        for b in self:
            b.population = len(b.npcs) + len(b.players)
    
    @api.depends('npcs')
    def _get_caps(self):
        for b in self:
            b.bottle_caps = 0 #Si no hay npcs, será 0
            for npc in b.npcs:
               b.bottle_caps += npc._get_caps()
    

    @api.model
    def create_random_bunker(self,vals):
        name = "Bunker "+str(random.randint(100, 120))
        food = random.randint(0,100)
        water = random.randint(0,100)
        water_deposits = random.randint(1,3)
        food_pantries = random .randint(1,3)
        max_population = water_deposits*5 + food_pantries*5

        for b in self:
            while b.name == name:
                name = "Bunker "+str(random.randint(100, 120))#Si el nombre coincide con los que ya hay, crea otro

        vals = {'name': name, 'food':food, 'water':water, 'water_deposits':water_deposits,
                    'food_pantries':food_pantries, 'max_population':max_population}
        res = super(bunker, self).create(vals)
        return res        
                
            
                

