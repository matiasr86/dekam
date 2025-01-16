from odoo import models, fields, api

class Box(models.Model):
    _name = 'dekam.box'
    _description = 'Box'

    name = fields.Char(string="Nombre")
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'box_id', string="Accesorios")
    high = fields.Float(string="Altura Cajón")
    depth = fields.Float(string="Profundidad")
    is_lateral_wood = fields.Boolean(string="Lateral de Madera?")
    lateral_wood = fields.Many2one('dekam.material' , string="Madera de Lateral")
    floor_wood = fields.Many2one('dekam.material', string="Madera de Piso")
    working_hours = fields.Float(string= "Horas de Trabajo")
    total_cost = fields.Float(string="Costo Total de la Orden", compute="_compute_total_cost", store=True)

    @api.depends('item_accessory_ids.total_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(item.total_cost for item in record.item_accessory_ids)