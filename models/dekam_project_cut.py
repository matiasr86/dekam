from odoo import models, fields, api
from odoo.addons.test_convert.tests.test_env import record


class ProjectCut(models.Model):
    _name = 'dekam.project.cut'
    _description = 'Cortes del Proyecto'

    name = fields.Char(string="Descripción", required=True)
    quantity = fields.Integer(string="Cantidad", required=True)
    wood = fields.Many2one('dekam.material',domain=[('isWood', '=', True)] , string="Madera", required=True)
    length = fields.Float (string="Largo", required=True)
    width = fields.Float (string="Ancho", required=True)
    squareMeters = fields.Float(string="Total m²", compute="_compute_square_meters", store=True)
    edge = fields.Many2one ('dekam.edge', string="Canto")
    left = fields.Boolean(string="Izquierdo")
    right = fields.Boolean(string="Derecho")
    top = fields.Boolean(string="Superior")
    bottom = fields.Boolean(string="Inferior")
    grain = fields.Char(string="Orientación Veta")
    module_id = fields.Many2one('dekam.module', string="Módulo")
    edgeMeters = fields.Float(string="Canto Mts", compute="_compute_edge_meters")
    project_id = fields.Many2one('dekam.project', string="Proyecto", ondelete="cascade")

    @api.depends('length', 'width')
    def _compute_square_meters(self):
        for record in self:
            # Convertir milímetros a metros y calcular el área
            record.squareMeters = (record.length / 1000) * (
                    record.width / 1000) * record.quantity if record.length and record.width else 0


