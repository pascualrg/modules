# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import image


class furgoneta(models.Model):
    _name = 'empresa.furgoneta'

    matricula = fields.Char()
    capacidad = fields.Integer()
    foto = fields.Image()

class paquete(models.Model):
    _name = 'empresa.paquete'

    id = fields.Char()
    volumen = fields.Integer()

class viaje(models.Model):
    _name = 'empresa.viaje'

    id = fields.Char()
    furgoneta = fields.One2many()
    paquetes = fields.One2many('empresa.paquete', 'viaje', readonly=True)

    teachers = fields.Many2many(comodel_name='empresa.conductor',
                                relation='teachers_classrooms',
                                column1='classroom_id',
                                column2='school_teacher_id')
    conductor = fields.One2many()





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
