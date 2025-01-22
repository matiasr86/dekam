from odoo import models, fields, api

class Accesory(models.Model):
    _name = 'dekam.accessory'
    _description = 'Accesorio'

    name = fields.Char(string="Nombre")
    lines = fields.One2many('dekam.line', 'accessory_id', string="Lineas")
    urls = fields.Many2many('dekam.url', 'accessory_id', string="Url Proveedores")
    cost_price = fields.Float (string="Precio de Costo")
    placementTime = fields.Float(string="Tiempo de Colocación (hs)")