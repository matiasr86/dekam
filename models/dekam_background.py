from odoo import models, fields, api

class Background(models.Model):
    _name = 'dekam.background'
    _description = 'Fondo'

    name = fields.Char(string="Nombre", required=True)
    wood = fields.Many2one('dekam.material',domain=[('isWood', '=', True)], string="Madera")
    background_type = fields.Selection(
        selection=[
            ('Ranurado', 'Ranurado'),
            ('Engrampado', 'Engrampado'),
            ('MDF Entarugado', 'MDF Entarugado'),
            ('Sin Fondo', 'Sin Fondo')
        ],
        string="Tipo de Fondo",
        required=True)
    work_hours = fields.Float(string="Horas de Trabajo", required=True)

