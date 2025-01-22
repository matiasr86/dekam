from odoo import models, fields, api

class ItemAccessory(models.Model):
    _name = 'dekam.item.accessory'
    _description = 'Item Accesorio'

    accessory_id = fields.Many2one('dekam.accessory', string="Accesorio", required=True)
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost", store=True)
    total_hours = fields.Float(string="Horas Totales", compute="_compute_total_hours", store=True)
    box_id = fields.Many2one('dekam.box', string="Cajón")
    module_id = fields.Many2one('dekam.module', string="Módulo")
    door_id = fields.Many2one('dekam.door', string="Módulo")


    @api.depends('accessory_id.cost_price', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * (record.accessory_id.cost_price or 0.0)

    @api.depends('accessory_id.placementTime', 'quantity')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = record.quantity * (record.accessory_id.placementTime or 0.0)