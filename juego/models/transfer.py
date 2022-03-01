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

class transfer(models.Model):
    _name = 'juego.transfer'
    _description = "'juego.transfer"

    name = fields.Char(compute='_get_name')

    npc1 = fields.Many2one('juego.npc')
    npc2 = fields.Many2one('juego.npc')

    caps_transfer_qty = fields.Integer(default="10")


    state = fields.Selection([('1', 'Chose NPCs'),('2', 'Select Quantity'), ('3', 'Finished Transfer')], default='1')

    date_transfer = fields.Datetime()


    @api.depends('npc1', 'npc2')
    def _get_name(self):
        for t in self:
            t.name = 'Transfer: '
            if t.npc1 and t.npc2:
                t.name = 'Transfer: '+ t.npc1.name + " to " + t.npc2.name

class create_transfer(models.TransientModel):
    _name = 'juego.create_transfer'
    _description = 'Create Transfer'

    name = fields.Char(compute='_get_name')

    
    npc1 = fields.Many2one('juego.npc')
    npc2 = fields.Many2one('juego.npc')

    npc1_caps = fields.Integer(compute="_get_npc1_caps")
    npc2_caps = fields.Integer(compute="_get_npc2_caps")

    npc1_name = fields.Char(compute="_get_npc1_name")
    npc2_name = fields.Char(compute="_get_npc2_name")

    caps_transfer_qty = fields.Integer(default="10")

    caps_transfer_qty_resume = fields.Integer(compute="_get_caps_transfer_qty_resume")


    state = fields.Selection([('1', 'Chose NPCs'),('2', 'Select Quantity'), ('3', 'Finish Transfer')], default='1')



    @api.depends('npc1', 'npc2')
    def _get_name(self):
        for t in self:
            t.name = 'Transfer: '
            if t.npc1 and t.npc2:
                t.name = 'Transfer: '+ t.npc1.name + " to " + t.npc2.name


    @api.depends('npc1')
    def _get_npc1_caps(self):
        self.npc1_caps = self.npc1.bottle_caps

    @api.depends('npc2')
    def _get_npc2_caps(self):
        self.npc2_caps = self.npc2.bottle_caps

    @api.depends('npc1')
    def _get_npc1_name(self):
        self.npc1_name = self.npc1.name

    @api.depends('npc2')
    def _get_npc2_name(self):
        self.npc2_name = self.npc2.name

    @api.depends('caps_transfer_qty')
    def _get_caps_transfer_qty_resume(self):
        self.caps_transfer_qty_resume = self.caps_transfer_qty


    #Solo se podran hacer transferencias entre NPCs que tengan un "Boss" (un player).
    @api.onchange('npc1')
    def _onchange_npc1(self):
        if self.npc1 != False:
            all_npcs = self.env['juego.npc'].search([]).filtered(lambda b: b.player)#NPCs que que pertenecen a un player
            npcs_libres =  all_npcs - self.npc1
            return {
                'domain': {
                    'npc2': [('id', 'in', npcs_libres.ids)],
                }
            }

    @api.onchange('npc2')
    def _onchange_npc2(self):
        if self.npc2 != False:
            all_npcs = self.env['juego.npc'].search([]).filtered(lambda b: b.player)#NPCs que que pertenecen a un player
            npcs_libres =  all_npcs - self.npc2
            return {
                'domain': {
                    'npc1': [('id', 'in', npcs_libres.ids)],
                }
            }
    ##################################################################################

    def next (self):
        if self.state == '1':

            if not self.npc1 or not self.npc2:
                raise ValidationError('Must have Origin and Receiver')
            else:
                self.state = '2'
        elif self.state == '2':

            if self.caps_transfer_qty<1 or self.caps_transfer_qty == "":
                raise ValidationError('Quantity cant be empty')
            else:
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


    def send_transfer(self):

        if self.npc1.bottle_caps<self.caps_transfer_qty:
            raise ValidationError("Insufficient funds from "+self.npc1.name+". Only have "+str(self.npc1.bottle_caps)+" and need "+str(self.caps_transfer_qty))
        else:
            #Resto al NPC origen las chapas de la transferencia
            self.npc1.bottle_caps = self.npc1.bottle_caps - self.caps_transfer_qty

            #Sumo al NPC destino las chapas de la transferencia
            self.npc2.bottle_caps = self.npc2.bottle_caps + self.caps_transfer_qty

            print("Transferencia enviada")
            transfer = self.env['juego.transfer'].create({
                'npc1': self.npc1.id,
                'npc2': self.npc2.id,
                'caps_transfer_qty' : self.caps_transfer_qty,
                'state': '3',
                'date_transfer' : datetime.now()
            })
            return {
                'name': 'Juego Transfer',
                'type': 'ir.actions.act_window',
                'res_model': 'juego.transfer',
                'res_id': transfer.id,
                'view_mode': 'form',
                'target': 'current'
            }