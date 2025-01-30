from odoo import models, fields, api

class Background(models.Model):
    _name = 'dekam.background'
    _description = 'Fondo'

    name = fields.Char(string="Nombre")
    wood = fields.Many2one('dekam.material',domain=[('isWood', '=', True)], string="Madera")
    work_hours = fields.Float(string="Horas de Trabajo")

