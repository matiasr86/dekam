from odoo import models, fields, api

class Module(models.Model):
    _name = 'dekam.module'
    _description = 'Modulo'

    name = fields.Char(string="Nombre")
    line = fields.Many2one('dekam.line' , string="Linea")
    wood = fields.Many2one('dekam.material' , string="Madera Caja")
    item_material_ids = fields.One2many('dekam.item.material', 'module_id', string="Materiales")
    complete_top = fields.Boolean(string="Tapa Superior?")
    strip_quantity = fields.Integer(string="Cantidad de Listones")
    rack_quantity = fields.Integer(string="Cantidad de Estantes")
    high = fields.Float (string="Alto")
    width = fields.Float (string="Ancho")
    depth = fields.Float (string="Profundidad")
    box_work_hours = fields.Float (string="Horas de Trabajo")
    item_box_ids = fields.One2many('dekam.item.box', 'module_id', string="Cajones")
    front_wood = fields.Many2one('dekam.material', string="Madera Frente")
    total_order_cost = fields.Float(string="Costo Total de la Orden", compute="_compute_total_order_cost", store=True)

    @api.depends('item_material_ids.total_cost')
    def _compute_total_order_cost(self):
        for record in self:
            record.total_order_cost = sum(item.total_cost for item in record.item_material_ids)

