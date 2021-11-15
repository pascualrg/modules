# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'


    name = fields.Char()
    classrooms = fields.Many2one('school.classroom', ondelete='set null')

class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'school.classroom'

    name = fields.Char()
    students = fields.One2many('school.student', 'classrooms')
    teachers = fields.Many2many('school.teacher')

class teacher (models.Model):
    _name = 'school.teacher'
    _description = 'school.teacher'

    name = fields.Char()
    classrooms = fields.Many2many('school.classroom')


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
