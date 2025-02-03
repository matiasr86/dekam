from odoo import models, fields, api

class DekamResumeEdge(models.Model):
    _name = "dekam.resume.edge"
    _description = "Resumen de Cantos por Material"

    module_id = fields.Many2one("dekam.module", string="Módulo", required=True)
    edge_id = fields.Many2one("dekam.edge", string="Canto", required=True)
    total_mt = fields.Float(string="Total mts")
    edge_cost = fields.Float(string="Total $", compute="_compute_edge_cost", store=True)

    @api.depends('total_mt', 'edge_id')
    def _compute_edge_cost(self):
        for record in self:
            record.edge_cost = (record.total_mt * record.edge_id.cost_price) * 1.10
            # 1.10 es el 10% adicional que representa el desperdicio


