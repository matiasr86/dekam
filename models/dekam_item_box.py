from odoo import models, fields, api

class ItemBox(models.Model):
    _name = 'dekam.item.box'
    _description = 'Item Cajón'

    box_id = fields.Many2one('dekam.box', string="Cajón", required=True)
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost", store=True)
    module_id = fields.Many2one('dekam.module', string="Módulo")

    @api.depends('box_id.cost_price', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * (record.box_id.cost_price or 0.0)