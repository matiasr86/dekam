from odoo import models, fields, api

class Door(models.Model):
    _name = 'dekam.door'
    _description = 'Door'

    name = fields.Char(string="Nombre")
    is_wood = fields.Boolean(string="En Madera?")
    elbow = fields.Float(string="Codo")
    light_horizontal = fields.Float(string="Luz en Horizontal")
    light_vertical = fields.Float(string="Luz en Vertical")
    edge = fields.Many2one('dekam.edge', string="Canto")
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'door_id', string="Accesorios")
    working_hours = fields.Float(string= "Horas de Trabajo")
    total_cost = fields.Float(string="Costo Total Puerta", compute="_compute_total_cost", store=True)

    @api.depends('item_accessory_ids.total_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(item.total_cost for item in record.item_accessory_ids)


