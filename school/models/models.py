# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import _
from odoo.exceptions import ValidationError, Warning
import secrets
import logging
import re
from odoo.exceptions import ValidationError
from odoo import http


_logger = logging.getLogger(__name__)

class banner_city_controller(http.Controller):
    @http.route('/school/banner', auth='user', type='json')
    def banner(self):
        return {
            'html': """
                <div  class="negocity_banner" 
                style="height: 280px; background-size:100%; background-image: url(/school/static/src/img/banner.jpg)">
                </div> """
        }

class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'


    name = fields.Char(required=True)
    birth_year = fields.Integer()

    test = fields.Boolean()

    #def _get_password(self): 
    #    return 

    enrollment_date = fields.Datetime(default=lambda self: fields.Datetime.now())
    last_login = fields.Datetime()
    password = fields.Char(default=lambda s:secrets.token_urlsafe(12))
    dni = fields.Char(string='DNI')
    profile_pic = fields.Image(max_width="50", max_height="50")
    is_student = fields.Boolean()
    classroom = fields.Many2one('school.classroom',  ondelete='set null', help='La clase a la que va el alumno')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)
    level = fields.Selection([('1','1'),('2','2')])

    state = fields.Selection([('1','Enrolled'),('2', 'Student'), ('3', 'Ex-Student')],default='1')

    @api.constrains('dni')
    def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z',re.I)
        for s in self:
            if regex.match(s.dni):
                print("Coincide")
            else:
                raise ValidationError('DNI incorrecto')

    _sql_constraints = [ ('dni_uniq','unique(dni)','El DNI no se puede repetir') ]

    def regenerate_pass(self):
        for s in self:
            password = secrets.token_urlsafe(12)
            s.write({'password':password})

    
class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'school.classroom'

    name = fields.Char()
    level = fields.Selection([('1','1'),('2','2')])
    students = fields.One2many(comodel_name='school.student', inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classrooms',
                                column1='classroom_id',
                                column2='school_teacher_id')

    all_teachers=fields.Many2many('school.teacher', compute='_get_teachers')

    def _get_teachers(self):
        for c in self:
            c.all_teachers = c.teachers
    

class teacher (models.Model):
    _name = 'school.teacher'
    _description = 'school.teacher'

    name = fields.Char()
    topic = fields.Char()
    phone = fields.Char()
    classrooms = fields.Many2many(comodel_name='school.classroom',
                                relation='teachers_classrooms',
                                column2='classroom_id',
                                column1='school_teacher_id')

