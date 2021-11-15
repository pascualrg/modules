# -*- coding: utf-8 -*-

import collections
from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'


    name = fields.Char()
    classroom = fields.Many2one('school.classroom', ondelete='set null', help='La clase a la que va el alumno')

class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'school.classroom'

    name = fields.Char()
    students = fields.One2many(comodel_name='school.student', inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classrooms',
                                column1='classroom_id',
                                column2='school_teacher_id')

class teacher (models.Model):
    _name = 'school.teacher'
    _description = 'school.teacher'

    name = fields.Char()
    classrooms = fields.Many2many(comodel_name='school.classroom',
                                relation='teachers_classrooms',
                                column2='classroom_id',
                                column1='school_teacher_id')

