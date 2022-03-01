from importlib.util import set_loader
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

class battle(models.Model):
    _name = 'juego.battle'
    _description = 'juego.battle'

    name = fields.Char(compute='_get_name')
    bunker1 = fields.Many2one('juego.bunker')
    bunker2 = fields.Many2one('juego.bunker')

    bunker1_team = fields.Many2many('juego.npc', compute="_get_npcs_from_bunker1")
    bunker2_team = fields.Many2many('juego.npc', compute="_get_npcs_from_bunker2")

    winner_name = fields.Char(string="Winner", readonly=True)
    loser_name = fields.Char(string="Loser", readonly=True)

    percentage_to_bet = fields.Float(default="10")


    caps_bet_qty = fields.Integer()

    state = fields.Selection([('1', 'Preparation'),('2', 'Start Battle'), ('3', 'Finished')], default='1')


    @api.depends('bunker1', 'bunker2')
    def _get_name(self):
        for b in self:
            b.name = 'Battle: '
            if b.bunker1 and b.bunker2:
                b.name = 'Battle: '+ b.bunker1.name + " VS " + b.bunker2.name


    @api.depends('bunker1')
    def _get_npcs_from_bunker1(self):

        self.bunker1_team = self.bunker1.npcs.ids

    @api.depends('bunker2')
    def _get_npcs_from_bunker2(self):

        self.bunker2_team = self.bunker2.npcs.ids


    @api.onchange('bunker1')
    def _onchange_bunker1(self):
        if self.bunker1 != False:
            bunkers = self.env['juego.bunker'].search([])
            bunkers_libres = bunkers - self.bunker1
            return {
                'domain': {
                    'bunker2': [('id', 'in', bunkers_libres.ids)],
                }
            }

    # @api.onchange('bunker1_team')
    # def _onchange_bunker1_team(self):

    #     print(self.bunker1.npcs.ids)
    #     npcs_del_bunker = self.bunker1.npcs

    #     # return {
    #     #         'domain': {
    #     #             'bunker1_team': [('id', 'in', self.bunker1.npcs.ids)],
    #     #         }
    #     #     }


    @api.depends('bunker1')
    def _get_npcs_from_bunker1(self):

        self.bunker1_team = self.bunker1.npcs.ids

    @api.depends('bunker2')
    def _get_npcs_from_bunker2(self):

        self.bunker2_team = self.bunker2.npcs.ids
    

            

    @api.onchange('bunker2')
    def _onchange_bunker2(self):
        if self.bunker2 != False:
            bunkers = self.env['juego.bunker'].search([])
            bunkers_libres = bunkers - self.bunker2
        
            return {
                'domain': {
                    'bunker1': [('id', 'in', bunkers_libres.ids)],
                }
            }

    def test(self):
        print("Pulsar en crear batalla")

#@api.constrains('bunker1','bunker2', ''

class create_battle(models.TransientModel):
    _name = 'juego.create_battle'
    _description = 'Create Battle'

    name = fields.Char(compute='_get_name')
    bunker1 = fields.Many2one('juego.bunker')
    bunker2 = fields.Many2one('juego.bunker')

    bunker1_team = fields.Many2many('juego.npc', compute="_get_npcs_from_bunker1")
    bunker2_team = fields.Many2many('juego.npc', compute="_get_npcs_from_bunker2")

    winner_name = fields.Char(string="Winner", readonly=True)
    loser_name = fields.Char(string="Loser", readonly=True)

    percentage_to_bet = fields.Float(default="10")

    caps_bet_qty = fields.Integer(compute="_get_bet_caps", string="Battle Staked Caps")

    state = fields.Selection([('1', 'Preparation'),('2', 'Start Battle'), ('3', 'Finished')], default='1')


    @api.depends('bunker1', 'bunker2')
    def _get_name(self):
        for b in self:
            b.name = 'Battle: '
            if b.bunker1 and b.bunker2:
                b.name = 'Battle: '+ b.bunker1.name + " VS " + b.bunker2.name


    @api.depends('bunker1_team', 'bunker2_team', 'percentage_to_bet' )
    def _get_bet_caps(self):
        for b in self:
            b.caps_bet_qty = 0
            if b.bunker1_team and b.bunker2_team:
                for team1Npc in b.bunker1_team:
                   b.caps_bet_qty += team1Npc.bottle_caps * (b.percentage_to_bet/100)

                for team2Npc in b.bunker2_team:
                   b.caps_bet_qty += team2Npc.bottle_caps * (b.percentage_to_bet/100)


    @api.depends('bunker1')
    def _get_npcs_from_bunker1(self):

        npcs_en_bunker = self.bunker1.npcs.filtered(lambda npc: npc.lugar == '2') #Solo muestra los npcs del bunker que estan en el mismo, si estan en una mision de busqueda, no sale en el desplegable

        self.bunker1_team = npcs_en_bunker.ids

    @api.depends('bunker2')
    def _get_npcs_from_bunker2(self):

        npcs_en_bunker = self.bunker2.npcs.filtered(lambda npc: npc.lugar == '2') #Solo muestra los npcs del bunker que estan en el mismo, si estan en una mision de busqueda, no sale en el desplegable

        self.bunker2_team = npcs_en_bunker.ids


    @api.onchange('bunker1')
    def _onchange_bunker1(self):
        if self.bunker1 != False:
            bunkers_con_player = self.env['juego.bunker'].search([]).filtered(lambda b: b.players)#Bunkers que ya tienen un player
            bunkers_libres = bunkers_con_player - self.bunker1
            return {
                'domain': {
                    #La lista del bunker 2 se elinará el bunker 1, para evitar peleas entre un mismo bunker.
                    'bunker2': [('id', 'in', bunkers_libres.ids)],
                }
            }

    @api.onchange('bunker2')
    def _onchange_bunker2(self):
        if self.bunker2 != False:
            bunkers_con_player = self.env['juego.bunker'].search([]).filtered(lambda b: b.players)#Bunkers que ya tienen un player
            bunkers_libres = bunkers_con_player - self.bunker2
            return {
                'domain': {
                    #La lista del bunker 1 se eliminará el bunker 2, para evitar peleas entre un mismo bunker.
                    'bunker1': [('id', 'in', bunkers_libres.ids)],
                }
            }

    def start_battle(self):
        print("Start")

        if self.percentage_to_bet < 5 or self.percentage_to_bet > 70:
            raise ValidationError('The percentage to bet must be between 5 and 70')
        else:

            qty_npcs_t1 = len(self.bunker1_team)
            qty_npcs_t2 = len(self.bunker2_team)

            #Creo una lista de numeros desde 0 a la cantidad de npcs que tiene el team 1
            boletos_t1 = list(range(0, qty_npcs_t1))
            #Creo otra desde la cantidad del team 1 a la cantidad de npcs que tiene el team 2
            boletos_t2 = list(range(qty_npcs_t1, qty_npcs_t2))

            #El total de posibilidades es la suma de todos los npcs
            oportunidades_totales = qty_npcs_t1 + qty_npcs_t2

            numRand = random.randint(0,oportunidades_totales-1)

            #Si el numero random se encuentra en la lista del team 1 será el ganador y el 2 el perdedor
            if numRand in boletos_t1:
                self.winner_name = "Bunker "+str(self.bunker1.name)
                self.loser_name = "Bunker "+str(self.bunker2.name)

                #Si gana el bunker 1, le quitaré el porcentaje de chapas a cada uno del bunker 2
                for team2Npc in self.bunker2_team:
                    team2Npc.bottle_caps  = team2Npc.bottle_caps - (team2Npc.bottle_caps *(self.percentage_to_bet/100))

                #Y sumaré el porcentaje al bunker 1
                for team1Npc in self.bunker1_team:
                    team1Npc.bottle_caps  = team1Npc.bottle_caps + (team1Npc.bottle_caps *(self.percentage_to_bet/100))
                

            else:
                self.winner_name = "Bunker "+str(self.bunker2.name)
                self.loser_name = "Bunker "+str(self.bunker1.name)

                #Sino, les quitare el porcentaje a los del bunker 1
                for team1Npc in self.bunker1_team:
                    team1Npc.bottle_caps  = team1Npc.bottle_caps - (team1Npc.bottle_caps *(self.percentage_to_bet/100))

                #Y sumaré el porcentaje al bunker 2
                for team2Npc in self.bunker2_team:
                    team2Npc.bottle_caps  = team2Npc.bottle_caps + (team2Npc.bottle_caps *(self.percentage_to_bet/100))

            #Contra más npcs tenga un equipo, más posibilidades de ganar

            #El porcentaje de chapas apostadas es sobre el número de chapas que tiene cada bunker, y se le sumará
            #o restara el portenaje sobre las chapas de cada uno

            self.state = '3'

            
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }


    def next (self):
        if self.state == '1':

            print(self.bunker1.id)
            if len(self.bunker1)>0 and len(self.bunker2)>0 and len(self.bunker1_team)>0 and len(self.bunker2_team)>0:
                self.state = '2'
            elif len(self.bunker1)<1 or len(self.bunker2)<1:
                raise ValidationError('Must choose two bunkers.')
            elif len(self.bunker1_team)<1 or len(self.bunker2_team)<1:
                raise ValidationError('The bunker must have npcs (Almost 1).')
            
        elif self.state == '2':
            self.state = '3'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def previous (self):
        if self.state == '2':
            self.state = '1'
        elif self.state == '3':
            self.state = '2'
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }


    def save_battle(self):
        print("Guardada")
        battle = self.env['juego.battle'].create({
            'bunker1': self.bunker1.id,
            'bunker2': self.bunker2.id,
            'bunker1_team' : self.bunker1_team.ids,
            'bunker1_team': self.bunker2_team.ids,
            'state': '3',
            'percentage_to_bet': self.percentage_to_bet,
            'winner_name' : self.winner_name,
            'loser_name' : self.loser_name,
            'caps_bet_qty' : self.caps_bet_qty

        })
        return {
            'name': 'Juego Battle',
            'type': 'ir.actions.act_window',
            'res_model': 'juego.battle',
            'res_id': battle.id,
            'view_mode': 'form',
            'target': 'current'
        }