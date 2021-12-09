# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import _
from odoo.exceptions import ValidationError, Warning
import secrets
import logging
import re
from odoo.exceptions import ValidationError
from odoo import http


class furgoneta(models.Model):
    _name = 'empresa.furgoneta'
    _description = 'empresa.furgoneta'

    

    matricula = fields.Char()
    name = fields.Char()
    capacidad = fields.Integer(string="Capadidad (m3)")
    foto = fields.Image()
    paquetes = fields.One2many(comodel_name='empresa.paquete', inverse_name='furgoneta', readonly=True)
    viajes = fields.One2many(comodel_name='empresa.viaje', inverse_name='furgoneta', readonly=True)

    

class paquete(models.Model):
    _name = 'empresa.paquete'
    _description = 'empresa.paquete'


    name = fields.Char()
    id = fields.Char()
    volumen = fields.Integer(string="Volumen (m3)")

    viaje = fields.Many2one('empresa.viaje',  ondelete='set null', help='El viaje donde va el paquete', readonly=True)
    furgoneta = fields.Many2one('empresa.furgoneta', related='viaje.furgoneta', ondelete='set null', help='La furgoneta donde va el paquete', readonly=True)

    def _get_volumen(self):
        return self.volumen


    

#un viaje solo una furgoneta
class viaje(models.Model):
    _name = 'empresa.viaje'
    _description = 'empresa.viaje'

    name = fields.Char()
    id = fields.Char()
    metros_aprovechados = fields.Integer(compute='_get_metros_aprovechados')
    furgoneta = fields.Many2one('empresa.furgoneta',  ondelete='set null', help='La furgoneta de este viaje')
    conductor = fields.Many2one('empresa.furgoneta',  ondelete='set null', help='La furgoneta de este viaje')

    
    paquetes = fields.One2many(comodel_name='empresa.paquete', inverse_name='viaje')

    
    def _get_metros_aprovechados(self):
        for m in self:
            m.metros_aprovechados = 0 #Si no hay npcs, será 0
            for paquete in m.paquetes:
               m.metros_aprovechados += paquete._get_volumen()

    @api.onchange('paquetes')
    def _onchange_paquetes(self):
        if self.furgoneta.capacidad < self.metros_aprovechados:
            raise ValidationError('Ya has llenado la furgoneta')

    





# class empresa(models.Model):
#     _name = 'empresa.empresa'
#     _description = 'empresa.empresa'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
