from pkg_resources import require

from odoo import models, fields, api

class Line(models.Model):
    _name = 'dekam.line'
    _description = 'Linea'

    name = fields.Char(string="Nombre", required=True)
    background = fields.Many2one('dekam.background' , string="Fondo")
    materialMargin = fields.Float(string="Margen Materiales %", required=True)
    accessoriesMargin = fields.Float(string="Margen Accesorios %", required=True)
    edgeMargin = fields.Float(string="Margen Canto %", required=True)
    workForceMargin = fields.Float(string="Margen Mano de Obra %", required=True)
    accessory_id = fields.Many2one('dekam.accessory', string="Accesorio")
    material_id = fields.Many2one('dekam.material', string="Material")
    door_id = fields.Many2one('dekam.door', string="Puerta")
    box_id = fields.Many2one('dekam.box', string="Cajón")
