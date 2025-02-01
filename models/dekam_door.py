from odoo import models, fields, api

class Door(models.Model):
    _name = 'dekam.door'
    _description = 'Door'

    name = fields.Char(string="Nombre", required=True)
    lines = fields.One2many('dekam.line', 'door_id', string="Lineas", required=True)
    is_wood = fields.Boolean(string="En Madera?")
    elbow = fields.Selection(
    [
        ('0', '0mm'),
        ('9', '9mm'),
        ('18','18mm')
    ],
    string="Codo",
    required=True)
    light_horizontal = fields.Float(string="Luz en Horizontal", required=True)
    light_vertical = fields.Float(string="Luz en Vertical", required=True)
    edge = fields.Many2one('dekam.edge', string="Canto", required=True)
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'door_id', string="Accesorios")
    working_hours = fields.Float(string= "Horas de Trabajo")
    total_workforce = fields.Float(string="Costo Mano de Obra", compute="_compute_total_workforce", store=True)
    total_hours = fields.Float(string="Horas Totales", compute="_compute_total_hours", store=True)
    total_cost = fields.Float(string="Costo Total (Sin Madera)", compute="_compute_total_cost", store=True)

    @api.depends('item_accessory_ids.total_cost', 'working_hours')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(item.total_cost for item in record.item_accessory_ids) + record.total_workforce


    @api.depends('total_hours')
    def _compute_total_workforce(self):
        for record in self:
            workforce = self.env['dekam.workforce'].search([], limit=1)
            cost_per_hour = workforce.cost_per_hour
            record.total_workforce = (record.total_hours * cost_per_hour)


    @api.depends('item_accessory_ids.total_hours')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = sum(item.total_hours for item in record.item_accessory_ids) + record.working_hours