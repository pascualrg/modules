# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import _
import random
#from odoo.exceptions import ValidationError, Warning
#import secrets
import logging
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo import http
import base64
import re


from odoo.tools import image

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
            print("Buscando npcs..")
            #npcs = self.env['juego.npc']._get_npcs()
    def find_bunker(self):
            print("Buscando bunker..")

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
        return self

        #return npcs



class bunker(models.Model):
    _name = 'juego.bunker'
    _description = 'juego.bunker'

    name = fields.Char(required=True)
    bImage = fields.Image(readonly=True, compute='_get_image_bunker_by_name')
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

    @api.constrains('name')
    def _check_dni(self):
        regex = re.compile('[0-9]{3}',re.I)
        for b in self:
            if regex.match(b.name) and (int(b.name) < 1000 and int(b.name) > 0): #el nombre del bunker tiene que ser un número entre 100 y 999
                print("Nombre correcto")
            else:
                raise ValidationError('Bunker name must be a number between 100 and 999')

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
    
    def _get_image_bunker_by_name(self):
        for b in self:
            #Meto el svg en un string
            bImageEnString = '<svg width="220px" height="220px" viewBox="0 0 220 220" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><title>Untitled</title><g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect id="Rectangle" stroke="#979797" fill="#262E3B" x="0.5" y="0.5" width="219" height="219"></rect><ellipse id="Oval" fill="#F8DC00" cx="109.5" cy="109.5" rx="68.5" ry="67.5"></ellipse><circle id="Oval" fill="#262E3B" cx="108" cy="110" r="55"></circle><ellipse id="Oval" stroke="#F8DC00" stroke-width="6" cx="109.5" cy="110" rx="75.5" ry="75"></ellipse><polygon id="Path" fill="#F8DC00" points="41.5529244 71.7262056 41.8509779 69.4758461 32.2913267 57.4566439 32.2913267 53.5469352 50.8652687 35.1152611 54.561354 35.1152611 65.7251758 44 68.9680867 44 42.1375082 72.8900547"></polygon><polygon id="º" fill="#F8DC00" transform="translate(107.629707, 29.002658) rotate(-315.000000) translate(-107.629707, -29.002658) " points="98.5529244 46.7262056 98.8509779 44.4758461 89.2913267 32.4566439 89.2913267 28.5469352 107.865269 10.1152611 111.561354 10.1152611 122.725176 19 125.968087 19 99.1375082 47.8900547"></polygon><polygon id="º" fill="#F8DC00" transform="translate(109.629707, 190.002658) rotate(-494.000000) translate(-109.629707, -190.002658) " points="100.552924 207.726206 100.850978 205.475846 91.2913267 193.456644 91.2913267 189.546935 109.865269 171.115261 113.561354 171.115261 124.725176 180 127.968087 180 101.137508 208.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(50.629707, 166.002658) rotate(-449.000000) translate(-50.629707, -166.002658) " points="41.5529244 183.726206 41.8509779 181.475846 32.2913267 169.456644 32.2913267 165.546935 50.8652687 147.115261 54.561354 147.115261 65.7251758 156 68.9680867 156 42.1375082 184.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(165.629707, 51.002658) rotate(-269.000000) translate(-165.629707, -51.002658) " points="156.552924 68.7262056 156.850978 66.4758461 147.291327 54.4566439 147.291327 50.5469352 165.865269 32.1152611 169.561354 32.1152611 180.725176 41 183.968087 41 157.137508 69.8900547"></polygon><polygon id="º" fill="#F8DC00" transform="translate(190.629707, 108.002658) rotate(-223.000000) translate(-190.629707, -108.002658) " points="181.552924 125.726206 181.850978 123.475846 172.291327 111.456644 172.291327 107.546935 190.865269 89.1152611 194.561354 89.1152611 205.725176 98 208.968087 98 182.137508 126.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(27.629707, 110.002658) rotate(-44.000000) translate(-27.629707, -110.002658) " points="18.5529244 127.726206 18.8509779 125.475846 9.29132673 113.456644 9.29132673 109.546935 27.8652687 91.1152611 31.561354 91.1152611 42.7251758 100 45.9680867 100 19.1375082 128.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(166.629707, 167.002658) rotate(-175.000000) translate(-166.629707, -167.002658) " points="157.552924 184.726206 157.850978 182.475846 148.291327 170.456644 148.291327 166.546935 166.865269 148.115261 170.561354 148.115261 181.725176 157 184.968087 157 158.137508 185.890055"></polygon><text id="101" font-family="Oswald-SemiBold, Oswald" font-size="48" font-weight="500" fill="#F8DC00"><tspan x="77.748" y="128">'+str(b.name)+'</tspan></text></g></svg>'
            #Codifico el string en formato ascii
            bImageEnAscii = bImageEnString.encode()
            #codifico el ascii en base64
            bImageFinal = base64.b64encode(bImageEnAscii)
            b.bImage = bImageFinal

    @api.model
    def create_random_bunker(self, vals):

        num = random.randint(100, 103)

        name = num
        food = random.randint(0,100)
        water = random.randint(0,100)
        water_deposits = random.randint(1,3)
        food_pantries = random .randint(1,3)
        max_population = water_deposits*5 + food_pantries*5

        #Meto el svg en un string
        bImageEnString = '<svg width="220px" height="220px" viewBox="0 0 220 220" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><title>Untitled</title><g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect id="Rectangle" stroke="#979797" fill="#262E3B" x="0.5" y="0.5" width="219" height="219"></rect><ellipse id="Oval" fill="#F8DC00" cx="109.5" cy="109.5" rx="68.5" ry="67.5"></ellipse><circle id="Oval" fill="#262E3B" cx="108" cy="110" r="55"></circle><ellipse id="Oval" stroke="#F8DC00" stroke-width="6" cx="109.5" cy="110" rx="75.5" ry="75"></ellipse><polygon id="Path" fill="#F8DC00" points="41.5529244 71.7262056 41.8509779 69.4758461 32.2913267 57.4566439 32.2913267 53.5469352 50.8652687 35.1152611 54.561354 35.1152611 65.7251758 44 68.9680867 44 42.1375082 72.8900547"></polygon><polygon id="º" fill="#F8DC00" transform="translate(107.629707, 29.002658) rotate(-315.000000) translate(-107.629707, -29.002658) " points="98.5529244 46.7262056 98.8509779 44.4758461 89.2913267 32.4566439 89.2913267 28.5469352 107.865269 10.1152611 111.561354 10.1152611 122.725176 19 125.968087 19 99.1375082 47.8900547"></polygon><polygon id="º" fill="#F8DC00" transform="translate(109.629707, 190.002658) rotate(-494.000000) translate(-109.629707, -190.002658) " points="100.552924 207.726206 100.850978 205.475846 91.2913267 193.456644 91.2913267 189.546935 109.865269 171.115261 113.561354 171.115261 124.725176 180 127.968087 180 101.137508 208.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(50.629707, 166.002658) rotate(-449.000000) translate(-50.629707, -166.002658) " points="41.5529244 183.726206 41.8509779 181.475846 32.2913267 169.456644 32.2913267 165.546935 50.8652687 147.115261 54.561354 147.115261 65.7251758 156 68.9680867 156 42.1375082 184.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(165.629707, 51.002658) rotate(-269.000000) translate(-165.629707, -51.002658) " points="156.552924 68.7262056 156.850978 66.4758461 147.291327 54.4566439 147.291327 50.5469352 165.865269 32.1152611 169.561354 32.1152611 180.725176 41 183.968087 41 157.137508 69.8900547"></polygon><polygon id="º" fill="#F8DC00" transform="translate(190.629707, 108.002658) rotate(-223.000000) translate(-190.629707, -108.002658) " points="181.552924 125.726206 181.850978 123.475846 172.291327 111.456644 172.291327 107.546935 190.865269 89.1152611 194.561354 89.1152611 205.725176 98 208.968087 98 182.137508 126.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(27.629707, 110.002658) rotate(-44.000000) translate(-27.629707, -110.002658) " points="18.5529244 127.726206 18.8509779 125.475846 9.29132673 113.456644 9.29132673 109.546935 27.8652687 91.1152611 31.561354 91.1152611 42.7251758 100 45.9680867 100 19.1375082 128.890055"></polygon><polygon id="º" fill="#F8DC00" transform="translate(166.629707, 167.002658) rotate(-175.000000) translate(-166.629707, -167.002658) " points="157.552924 184.726206 157.850978 182.475846 148.291327 170.456644 148.291327 166.546935 166.865269 148.115261 170.561354 148.115261 181.725176 157 184.968087 157 158.137508 185.890055"></polygon><text id="101" font-family="Oswald-SemiBold, Oswald" font-size="48" font-weight="500" fill="#F8DC00"><tspan x="77.748" y="128">'+str(num)+'</tspan></text></g></svg>'
        #Codifico el string en formato ascii
        bImageEnAscii = bImageEnString.encode()
        #codifico el ascii en base64
        bImage = base64.b64encode(bImageEnAscii)
        
        for b in self:
            if b.name == name:
                num = random.randint(101, 120)
                name = num #Si el nombre coincide con los que ya hay, crea otro

        vals = {'name': name, 'food':food, 'water':water, 'water_deposits':water_deposits,
                    'food_pantries':food_pantries, 'max_population':max_population, 'bImage':bImage}
        res = super(bunker, self).create(vals)
        return res
                
            
                

