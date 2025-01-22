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
    accessory_id = fields.Many2one('dekam.accessory', string="Accesorio")
    material_id = fields.Many2one('dekam.material', string="Material")
    door_id = fields.Many2one('dekam.door', string="Puerta")
    box_id = fields.Many2one('dekam.box', string="Cajón")
