from odoo import models, fields, api

class WorkForce(models.Model):
    _name = 'dekam.workforce'
    _description = 'WorkForce'

    name = fields.Char(string="Nombre")
    cost_per_hour = fields.Float(string="Costo por Hora")
