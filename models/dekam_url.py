from odoo import models, fields, api

class Url(models.Model):
    _name = 'dekam.url'
    _description = 'Url'

    name = fields.Char(string="Proveedor")
    url = fields.Char(string="Url")
    material_id = fields.Many2one('dekam.material', string="Material")
    accessory_id = fields.Many2one('dekam.accessory', string="Accesorio")