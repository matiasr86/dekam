from odoo import models, fields, api

class ItemDoor(models.Model):
    _name = 'dekam.item.door'
    _description = 'Item Puerta'

    door_id = fields.Many2one('dekam.door', string="Puerta", required=True)
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost", store=True)
    module_id = fields.Many2one('dekam.module', string="Módulo")



    @api.depends('door_id.total_cost', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * (record.door_id.total_cost or 0.0)