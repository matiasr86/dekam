from odoo import models, fields, api

class ItemMaterial(models.Model):
    _name = 'dekam.item.material'
    _description = 'Item Material'

    material_id = fields.Many2one('dekam.material', string="Material", required=True)
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost", store=True)
    module_id = fields.Many2one('dekam.module', string="Módulo")

    @api.depends('material_id.cost_price', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * (record.material_id.cost_price or 0.0)