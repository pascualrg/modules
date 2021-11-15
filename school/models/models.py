# -*- coding: utf-8 -*-

from odoo import models, fields, api
import secrets

class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'


    name = fields.Char(required=True)
    birth_year = fields.Integer()
    password = fields.Char(compute='_get_password', store=True)
    classroom = fields.Many2one('school.classroom', ondelete='set null', help='La clase a la que va el alumno')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

    @api.depends('name')
    def _get_password(self):
        print(self)
        for student in self:
            print(student)
            student.password = secrets.token_urlsafe(12)

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

