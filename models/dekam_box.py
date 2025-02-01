from odoo import models, fields, api

class Box(models.Model):
    _name = 'dekam.box'
    _description = 'Box'

    name = fields.Char(string="Nombre", required=True)
    lines = fields.One2many('dekam.line', 'box_id', string="Lineas", required=True)
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'box_id', string="Accesorios", required=True)
    item_material_ids = fields.One2many('dekam.item.material', 'box_id', string="Materiales", required=True)
    high = fields.Float(string="Altura Cajón", required=True)
    depth = fields.Float(string="Profundidad", required=True)

    lateral_space = fields.Float(string="Luz Lateral", required=True)
    top_space = fields.Float(string="Luz Superior", required=True)
    between_box_space = fields.Float(string="Luz entre Cajones", required=True)
    with_profile = fields.Boolean(string="Con Perfil?")
    profile_size = fields.Float(string="Medida Perfil")
    slide_space = fields.Float(string="Espacio Int. Corredera")

    is_lateral_wood = fields.Boolean(string="Lateral de Madera?")
    lateral_wood = fields.Many2one('dekam.material' , string="Madera de Lateral")

    floor_wood = fields.Many2one('dekam.material', string="Madera de Piso" , required=True)
    type_union_floor = fields.Selection([
        ('grooved', 'Ranurado'),
        ('doweled', 'Entarugado')
    ], string="Piso Tipo")
    floor_length = fields.Float(string="Ancho de Piso (AI - ?)")
    floor_depth = fields.Float(string="Profundidad de Piso (LN - ?)")

    back_facade_length = fields.Float(string="Contra Frente (AI - ?)")
    edge_front = fields.Many2one('dekam.edge', string="Canto de Tapa")
    edge_box = fields.Many2one('dekam.edge', string="Canto de Caja")


    working_hours = fields.Float(string= "Madera (Horas de Trabajo)", required=True)
    total_accessorys = fields.Float(string="Costo Accesorios", compute="_compute_total_accessory", store=True)
    total_materials = fields.Float(string="Costo Materiales", compute="_compute_total_material", store=True)
    total_hours = fields.Float(string="Horas Totales", compute="_compute_total_hours", store=True)
    total_workforce = fields.Float(string="Costo Mano de Obra", compute="_compute_total_workforce", store=True)
    total_cost = fields.Float(string="Costo Total (Sin Madera)", compute="_compute_total_cost", store=True)


    @api.depends('item_accessory_ids.total_cost')
    def _compute_total_accessory(self):
        for record in self:
            record.total_accessorys = sum(item.total_cost for item in record.item_accessory_ids)

    @api.depends('item_material_ids.total_cost')
    def _compute_total_material(self):
        for record in self:
            record.total_materials = sum(item.total_cost for item in record.item_material_ids)

    @api.depends('total_accessorys', 'total_workforce', 'total_materials')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.total_accessorys + record.total_workforce + record.total_materials

    @api.depends('item_accessory_ids.total_hours')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = sum(item.total_hours for item in record.item_accessory_ids) + record.working_hours

    @api.depends('total_hours')
    def _compute_total_workforce(self):
        for record in self:
            workforce = self.env['dekam.workforce'].search([], limit=1)
            cost_per_hour = workforce.cost_per_hour
            record.total_workforce = (record.total_hours * cost_per_hour)