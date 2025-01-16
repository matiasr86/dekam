from odoo import models, fields, api

class Box(models.Model):
    _name = 'dekam.box'
    _description = 'Box'

    name = fields.Char(string="Nombre")
    high = fields.Float(string="Altura Cajón")
    cost_price = fields.Float (string="Precio de Costo")
    working_hours = fields.Float(string= "Horas de Trabajo")