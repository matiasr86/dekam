from odoo import models, fields, api

class ItemModule(models.Model):
    _name = 'dekam.item.module'
    _description = 'Item Modulo'

    module_id = fields.Many2one('dekam.module', string="Modulo", required=True)
    quantity = fields.Float(string="Cantidad", required=True, default=1.0)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost", store=True)
    total_hours = fields.Float(string="Horas Totales", compute="_compute_total_hours", store=True)
    project_id = fields.Many2one('dekam.project', string="Proyecto", ondelete="cascade")




    @api.depends('module_id.total_cost', 'quantity')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * (record.module_id.total_cost or 0.0)

    @api.depends('module_id.total_hours', 'quantity')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = record.quantity * (record.module_id.total_hours or 0.0)