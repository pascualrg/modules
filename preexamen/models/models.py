# -- coding: utf-8 --

from operator import truediv
from odoo import models, fields, api
from pymacaroons import Macaroon

class cliente(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    #canciones = fields.One2many('preexamen.cancion', 'clientes', readonly=True)

    canciones = fields.Many2many(comodel_name='preexamen.cancion',
                                relation='canciones_clientes',
                                column2='cliente_id',
                                column1='cancion_id')
class cancion(models.Model):
    _name = 'preexamen.cancion'
    _description = 'Cancion'

    name = fields.Char(string="Nombre",required=True)
    artista = fields.Char(string="Artista",required=True)
    popularidad = fields.Integer()

    #clientes = fields.Many2one(string='Clientes', comodel_name='res.partner', ondelete='set null')

    clientes = fields.Many2many(comodel_name='res.partner',
                                relation='canciones_clientes',
                                column1='cliente_id',
                                column2='cancion_id')


    def bajar_popu(self):
        print("Bajando popularidad..")
        canciones = self.search([])
        for c in canciones:
            #Si ya no tiene popularidad, no bajara de 0
            if(c.popularidad>0):
                c.popularidad -= 1

class cancion_wizard(models.TransientModel):
    _name = 'preexamen.cancion_wizard'

    cancion = fields.Many2one('preexamen.cancion', required="True")

    cliente = fields.Many2one('res.partner', compute="_get_cliente")

    @api.model
    def action_cancion_wizard(self):
        action = self.env.ref('preexamen.action_cancion_wizard').read()[0]
        return action

    @api.depends('cancion')
    def _get_cliente(self):

        clienteID = self.env.context.get('cliente_id')
        cliente = self.env['res.partner'].search([]).filtered(lambda a: a.id ==clienteID)
        
        for c in self:
            c.cliente = cliente[0].id
        

    def cancion_favorita(self):
        clienteID = self.env.context.get('cliente_id')
        cliente = self.env['res.partner'].search([]).filtered(lambda a: a.id ==clienteID)
        #print(cliente[0].name)

        #Añado la cancion al cliente y el cliente a la cancion
        self.write({'cliente':[(4,clienteID)]})
        cliente[0].write({'canciones':[(4,self.cancion.id)]})
        
        #Sumo 100 cada vez que alguien le de a favorito
        self.cancion.popularidad += 100
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': clienteID,
            'view_mode': 'form',
            'view_id' : self.env.ref('preexamen.cliente_form').id,
            'target': 'current',
        }                
