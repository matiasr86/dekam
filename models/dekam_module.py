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
    box_work_hours = fields.Float(string="Horas de Fabricación (Caja)")
    item_door_ids = fields.One2many('dekam.item.door', 'module_id', string="Puertas")
    total_cost_door = fields.Float(string="Costo Total de la Puerta", compute="_compute_total_cost_door", store=True)
    item_box_ids = fields.One2many('dekam.item.box', 'module_id', string="Cajones")
    total_cost_box = fields.Float(string="Costo Total de la Cajones", compute="_compute_total_cost_box", store=True)
    front_wood = fields.Many2one('dekam.material', string="Madera Frente")
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'module_id', string="Accesorios")
    total_cost = fields.Float(string="Costo Total del Módulo", compute="_compute_total_cost", store=True)

    @api.depends('item_material_ids.total_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(item.total_cost for item in record.item_material_ids)


    @api.depends('item_door_ids.total_cost')
    def _compute_total_cost_door(self):
        for record in self:
            record.total_cost_door = sum(item.total_cost for item in record.item_door_ids)

    @api.depends('item_box_ids.total_cost')
    def _compute_total_cost_box(self):
        for record in self:
            record.total_cost_box = sum(item.total_cost for item in record.item_box_ids)