from odoo import models, fields, api

class ItemBox(models.Model):
    _name = 'dekam.item.box'
    _description = 'Item Cajón'

    box = fields.Many2one('dekam.box', string="Cajón", required=True)
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost", store=True)
    total_hours = fields.Float(string="Horas Totales", compute="_compute_total_hours", store=True)
    module_id = fields.Many2one('dekam.module', string="Módulo")


    @api.depends('box.total_cost', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * (record.box.total_cost or 0.0)

    @api.depends('box.total_hours', 'quantity')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = record.quantity * (record.box.total_hours or 0.0)