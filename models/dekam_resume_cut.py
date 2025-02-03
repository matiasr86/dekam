from odoo import models, fields, api

class DekamResumeCut(models.Model):
    _name = "dekam.resume.cut"
    _description = "Resumen de Cortes por Material"

    module_id = fields.Many2one("dekam.module", string="Módulo", required=True)
    material_id = fields.Many2one("dekam.material", string="Material", required=True)
    total_m2 = fields.Float(string="Total m²")
    material_cost = fields.Float(string="Total $", compute="_compute_material_cost", store=True)
    wood_quantity = fields.Float(string="Placas", compute="_compute_wood_quantity", store=True)


    @api.depends('total_m2', 'material_id')
    def _compute_material_cost(self):
        for record in self:
            record.material_cost = (record.total_m2 * record.material_id.squareMetersPrice) * 1.10
            # 1.10 es el 10% adicional que representa el desperdicio

    @api.depends('total_m2', 'material_id')
    def _compute_wood_quantity(self):
        for record in self:
            record.wood_quantity = round((record.total_m2 * 1.10) / ((record.material_id.length * record.material_id.width) / 1000000), 2)
            # 1.10 es el 10% adicional que representa el desperdicio

