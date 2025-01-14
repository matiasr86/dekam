from odoo import models, fields, api


class Cut(models.Model):
    _name = 'dekam.cut'
    _description = 'Cortes'

    name = fields.Char(string="Descripción")
    quantity = fields.Integer(string="Cantidad")
    length = fields.Float (string="Largo")
    width = fields.Float (string="Ancho")
    squareMeters = fields.Float(string="Mts2", compute="_compute_square_meters", store=True)
    edge = fields.Many2one ('dekam.edge', string="Canto")
    left = fields.Boolean(string="Izquierdo")
    right = fields.Boolean(string="Derecho")
    top = fields.Boolean(string="Superior")
    bottom = fields.Boolean(string="Inferior")

    @api.depends('length', 'width')
    def _compute_square_meters(self):
        for record in self:
            # Convertir milímetros a metros y calcular el área
            record.squareMeters = (record.length / 1000) * (
                        record.width / 1000) if record.length and record.width else 0


