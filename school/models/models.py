# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo import _
from odoo.exceptions import Warning
import secrets
import logging

_logger = logging.getLogger(__name__)

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
            #print('\033[93m]',student,'\033[93m]')
            student.password = secrets.token_urlsafe(12)
            _logger.debug('\033[93m]'+str(student)+'\033[93m]')

class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'school.classroom'

    name = fields.Char()
    students = fields.One2many(comodel_name='school.student', inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classrooms',
                                column1='classroom_id',
                                column2='school_teacher_id')

    delegate=fields.Many2one('school.student',compute='_get_delegate')
    all_teachers=fields.Many2many('school.teacher', compute='_get_teachers')

    def _get_delegate(self):
        for c in self:
            c.delegate = c.students[0].id
    def _get_teachers(self):
        for c in self:
            c.all_teachers = c.teachers
    

class teacher (models.Model):
    _name = 'school.teacher'
    _description = 'school.teacher'

    name = fields.Char()
    classrooms = fields.Many2many(comodel_name='school.classroom',
                                relation='teachers_classrooms',
                                column2='classroom_id',
                                column1='school_teacher_id')

