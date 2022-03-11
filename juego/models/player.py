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


class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    have_explorer_pass = fields.Boolean(string="Purchased")

    is_player = fields.Boolean(default=False)
    username = fields.Char(required=True)
    #name = fields.Char(required=True)
    password = fields.Char(required=True)

    def _get_random_avatar(self):
            print("test")
            num = random.randint(1, 20)
            img = open("juego/static/src/img/players_default/player_default_"+str(num)+".svg", "rb")
            imgLeer = img.read()
            return base64.b64encode(imgLeer)

    avatar = fields.Image(max_width=200, max_height=200, default=_get_random_avatar)
    birth_year = fields.Integer(default="2003")
    register_date = fields.Datetime(default=lambda self:fields.Datetime.now(), store=True, readonly=True)
    level = fields.Integer(readonly=True)
    lugar = fields.Selection([('1','Wasteland'),('2', 'Bunker')],default='1')


    npcs = fields.One2many('juego.npc', 'player', readonly=True)
    bunker = fields.Many2one('juego.bunker', ondelete='restrict', readonly=True)
    bunkerImg = fields.Image(related='bunker.bImage')

    _sql_constraints = [ ('username_uniq','unique(username)','The username is in use, choose another.') ]

    @api.depends('level', 'have_explorer_pass')
    def _get_max_npcs(self):
        if self.have_explorer_pass:
            for p in self:
                p.max_npcs = 10+self.level #Si tiene el explorer pass, su base de npcs maximos será 10 (más el nivel)
        else:
            for p in self:
                p.max_npcs = 5+self.level #Sino, su base de npcs maximos será 5 (más el nivel)

    max_npcs = fields.Integer(compute='_get_max_npcs', readonly=True)

    @api.onchange('birth_year')
    def _onchange_birth_year(self):
        now = datetime.now()
        if self.birth_year > (now.year - 18):
            self.birth_year = now.year - 18
            return {'warning':{'title':'Insufficient age', 'message':'You must be of legal age to play (18)'}}
            

    def recruit_npc(self):
            #Antes de poder apretar el botón reclutar, se tendrá que "buscar" un bunker
            #cuendo encuentre el bunker, pasará de estado "yermo" a estado "bunker"
            #Luego, ya con bunker, se le creará un npc, el cual "vivirá" en el mismo bunker.
            #Si en el bunker no hay espacio, el jugador no podrá tener npc
            print("Buscando npcs..")

            npc_object = self.env['juego.npc']
            all_npc_object = npc_object.search([])

            bunker_pop = self.bunker.population
            bunker_max_pop = self.bunker.max_population
            print(bunker_pop)
            print(bunker_max_pop)

            if bunker_pop < bunker_max_pop:

                if len(self.npcs) < self.max_npcs:

                    if all_npc_object:
                        quedanNpc = False
                        repetido = True

                        for npc in all_npc_object:
                                #print(npc.player)
                                if not npc.player:#Si no hay un jugador en algun npc, quedanNpc = verdadero
                                    quedanNpc=True

                        if not quedanNpc:#Si no quedan npcs que asignar avisará
                            raise ValidationError('No quedan NPCs que asignar')
                        else:
                            while repetido:
                                num_random = random.randint(0, (len(all_npc_object)-1))
                                if not all_npc_object[num_random].player:
                                    print("Se ha asignado: "+all_npc_object[num_random].name)
                                    all_npc_object[num_random].player = self
                                    all_npc_object[num_random].bunker = self.bunker
                                    all_npc_object[num_random].lugar = '2'
                                    repetido=False
                                else:
                                    #print("Ya esta asignado")
                                    if not quedanNpc:
                                        repetido=False
                                        raise ValidationError('No quedan NPCs que asignar')
                else:
                    raise UserError('The player have not permissions to get more npcs [Actual limit: '+str(self.max_npcs)+']. You can upgrade this with explorer pass or leveling up.')
                    return {'warning':{'title':'Max NPCs for player reached', 'message':'The player have not permissions to get more npcs, you can upgrade this with explorer pass or leveling up.'}}
            else:
                raise UserError('This bunker has reached its maximum capacity, upgrade it to recruit new npc.')
                return {'warning':{'title':'Full bunker', 'message':'This bunker has reached its maximum capacity, upgrade it to recruit new npc.'}}
        

    def find_bunker(self):
        
        all_bunkers = self.env['juego.bunker'].search([])#Todos los bunkers
        bunkers_con_player = self.env['juego.bunker'].search([]).filtered(lambda b: b.players)#Bunkers que ya tienen un player
        bunkers_libres = all_bunkers-bunkers_con_player#Bunkers que aun no tienen un player

        if len(all_bunkers) > len(bunkers_con_player):
            # for b_con_p in bunkers_con_player:
            #     print(b_con_p.id)

            # for b_libres in bunkers_libres:
            #     print(b_libres.id)

            num_random = random.randint(0, (len(bunkers_libres)-1)) #numero random desde 0 hasta el numero de bunkers libres - 1
            
            self.bunker = bunkers_libres[num_random] #Asigno el bunker random al campo bunker del player
            self.lugar = '2' #Cambio el estado de 'yermo' a 'bunker'
        else:
            raise ValidationError('No hay bunkers donde ir')

    
    def leave_bunker(self):
        self.write({'bunker': [(5, 0, 0)]})#'elimino' o 'limpio' el campo bunker del jugador
        self.lugar = '1' #Cambio el estado de 'bunker' a 'yermo'
        self.write({'npcs': [(5, 0, 0)]})#Se considerá que abandona a los npcs en el bunker
        #raise ValidationError('Todos los NPCs abandonaron al jugado al salir este del bunker')

    def gen_random_avatar(self):
            print("test")
            num = random.randint(1, 20)
            img = open("juego/static/src/img/players_default/player_default_"+str(num)+".svg", "rb")
            imgLeer = img.read()
            for p in self:
                p.write({'avatar':base64.b64encode(imgLeer)})

    def buy_explorer_pass(self):
        if not self.have_explorer_pass:
            self.have_explorer_pass = True

    @api.model
    def update_players_progress(self):
        players = self.search([])
        date = fields.datetime.now()
        for p in players:

            if self.have_explorer_pass:
                numRand = random.randint(1,5)
            else:
                numRand = random.randint(0,3)

            
            p.level = p.level + numRand #cada día del juego, subiran niveles aleatoriamente.
            #print(p.level)
            self.env['juego.player_progress'].create({'name': p.level, 'player': p.id, 'date_char': date})

    def show_player_progress(self):
        return {
            'name': 'Player level progress',
            'type': 'ir.actions.act_window',
            'res_model': 'juego.player_progress',
            'view_mode': 'graph',
            'target': 'new',
            'context':  self._context,
            'domain': [('player', '=', self.id)]
        }


class player_progress(models.Model):
    _name = 'juego.player_progress'
    _description = 'Players progress'

    name = fields.Integer(string='Level')
    date_char = fields.Char(default= lambda d: fields.datetime.now())
    player = fields.Many2one('res.partner')