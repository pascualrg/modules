# -- coding: utf-8 --

from operator import truediv
from odoo import models, fields, api


class colegio(models.Model):
    _name = 'preexamen.colegio'
    _description = 'Colegio'

    name = fields.Char(string="Nombre",required=True)
    clases = fields.One2many(string='Clases',comodel_name='preexamen.clase',inverse_name='colegio')
    alumnos = fields.One2many(string='Alumnos',comodel_name='res.partner',inverse_name='colegio')
    profesores = fields.One2many(string='Profesores',comodel_name='preexamen.profesor',inverse_name='colegio')

class clase(models.Model):
    _name = 'preexamen.clase'
    _description = 'Clase'

    name = fields.Char(string="Nombre",required=True)
    colegio = fields.Many2one('preexamen.colegio', required="True")
    alumnos = fields.One2many(string='Alumnos',comodel_name='res.partner',inverse_name='clase',  readonly=True)
    profesores = fields.Many2many(comodel_name='preexamen.profesor',
                                relation='clases_profesores',
                                column2='clase_id',
                                column1='preexamen_profesor_id',  readonly=True)

class alumno(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    name = fields.Char(string="Nombre",required=True)
    es_alumno = fields.Boolean(compute="_get_es_alumno", store=True, default=False)
    colegio = fields.Many2one('preexamen.colegio', compute='_get_colegio')
    clase = fields.Many2one('preexamen.clase', required="True")
    profesores = fields.Many2many('preexamen.profesor', related='clase.profesores', readonly=True)
    dias_cursados = fields.Integer()

    @api.model
    def contar_dias(self):
        alumnos = self.search([])
        for a in alumnos:
            if(a.es_alumno):
                a.dias_cursados += 1

    @api.depends('clase')
    def _get_colegio(self):
        for a in self:
            a.colegio = a.clase.colegio

    def _get_es_alumno(self):
        for a in self:
            if(a.clase):
                a.es_alumno = True
            else:
                a.es_alumno = False

    def reset_dias(self, records):
        for a in records:
            a.dias_cursados = 0

    def mostrar_mas_dias(self):
        todos_alumnos = self.env['res.partner'].search([]).filtered(lambda a: a.es_alumno)

        alumno_con_mas_dias = todos_alumnos.sorted(key=lambda a: a.dias_cursados, reverse=True)

        print(alumno_con_mas_dias[0].name)

        # return {
        #     'name': 'Alumno con mas dias',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'res.partner',
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('preexamen.alumno_form').id,
        #     'target': 'current',
        #     'context':  self._context,
        #     'domain': [('alumno', '=', alumno_con_mas_dias[0].id)]
        # }



class profesor(models.Model):
    _name = 'preexamen.profesor'
    _description = 'Profesor'

    name = fields.Char(string="Nombre",required=True)
    colegio = fields.Many2one('preexamen.colegio', required="True")
    clases = fields.Many2many(comodel_name='preexamen.clase',
                                relation='clases_profesores',
                                column1='clase_id',
                                column2='preexamen_profesor_id')

    alumnos = fields.Many2many('res.partner', compute='_get_alumnos', readonly=True)

    def _get_alumnos(self):
        for p in self:
            for c in p.clases:
                p.alumnos += c.alumnos

class alumno_wizard(models.TransientModel):
    _name = 'preexamen.alumno_wizard'

    name = fields.Char(string="Nombre",required=True)

    @api.model
    def action_alumno_wizard(self):
        action = self.env.ref('preexamen.action_alumno_wizard').read()[0]
        return action

    def create_alumno(self):
        clase = self.env.context.get('clase_id')
        for c in self:
            alumno_nuevo = c.env['res.partner'].create({'name': c.name,'clase':clase, 'es_alumno':True})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': alumno_nuevo.id,
            'view_mode': 'form',
            'view_id' : self.env.ref('preexamen.alumno_form').id,
            'target': 'current',
        }                



# class clase_wizard(models.TransientModel):

#     _name = 'preexamen.clase_wizard'

#     state = fields.Selection([('1','Clase'),('2','Profesor'),('3','Alumno')],default='1')
#     name = fields.Char()
#     c_name = fields.Char(string='Nombre Clase')
#     c_colegio = fields.Many2one('preexamen.colegio', required="True")
    
#     p_name = fields.Char(string='Nombre Profesor')
#     a_name = fields.Char(string='Nombre Alumno')


#     @api.model
#     def action_course_wizard(self):
#         action = self.env.ref('preexamen.action_clase_wizard').read()[0]
#         return action

#     def next(self):
#         if self.state == '1':
#             self.state = '2'
#         elif self.state == '2':
#             self.state = '3'
#         return {
#                 'type': 'ir.actions.act_window',
#                 'res_model': self._name,
#                 'res_id': self.id,
#                 'view_mode': 'form',
#                 'target': 'new',
#             }
#     def previous(self):
#         if self.state == '2':
#             self.state = '1'
#         elif self.state == '3':
#             self.state = '2'
#         elif self.state == '4':
#             self.state = '3'
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': self._name,
#             'res_id': self.id,
#             'view_mode': 'form',
#             'target': 'new',
#         }

#     def add_classroom(self):
#         for c in self:
#             c.write({'classrooms':[(0,0,{'name':c.c_name,'level':c.c_level})]})
#             return {
#                 'type': 'ir.actions.act_window',
#                 'res_model': self._name,
#                 'res_id': self.id,
#                 'view_mode': 'form',
#                 'target': 'new',
#             }


#     def commit(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': self._name,
#             'res_id': self.id,
#             'view_mode': 'form',
#             'target': 'new',
#         }

#     def create_course(self):
#         for c in self:
#             curs = c.env['school.course'].create({'name': c.name})
#             students = []
#             for cl in c.classrooms:
#                 classroom = c.env['school.classroom'].create({'name':cl.name,'course':curs.id,'level':cl.level})
#                 for st in cl.students:
#                     student=c.env['res.partner'].create({'name': st.name,
#                                                         'dni': st.dni,
#                                                         'birth_year': st.birth_year,
#                                                         'is_student':True,
#                                                         'classroom': classroom.id
#                                                         })
#                     students.append(student.id)
#                     curs.write({'students':[(6,0,students)]})

#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'school.course',
#             'res_id': curs.id,
#             'view_mode': 'form',
#             'target': 'current',
#         }

# class classroom_aux(models.TransientModel):
# 	_name = 'school.classroom_aux'
# 	name = fields.Char()
# 	level = fields.Selection([('1', '1'), ('2', '2')])
# 	students = fields.One2many('school.student_aux','classroom')

# class student_aux(models.TransientModel):
# 	_name = 'school.student_aux'
# 	name = fields.Char()
# 	birth_year = fields.Integer()
# 	dni = fields.Char(string='DNI')
# 	classroom = fields.Many2one('school.classroom_aux')


