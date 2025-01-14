from odoo import models, fields, api

class Line(models.Model):
    _name = 'dekam.line'
    _description = 'Linea'

    name = fields.Char(string="Nombre")
    background = fields.Many2one('dekam.background' , string="Fondo")
    materialMargin = fields.Float(string="Margen Materiales %")
    accessoriesMargin = fields.Float(string="Margen Accesorios %")
    edgeMargin = fields.Float(string="Margen Canto %")
    workForceMargin = fields.Float(string="Margen Mano de Obra %")
