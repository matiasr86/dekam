from odoo import models, fields, api

class Edge(models.Model):
    _name = 'dekam.edge'
    _description = 'Canto'

    name = fields.Char(string="Nombre")
    thickness = fields.Float(string="Espesor (mm)")
    width = fields.Float(string="Ancho (mm)")
    urls = fields.Many2many('dekam.url',  string="Url Proveedores")
    cost_price = fields.Float (string="Costo x Metro")

