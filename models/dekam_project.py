from odoo import models, fields, api

class Project(models.Model):
    _name = 'dekam.project'
    _description = 'Project'

    name = fields.Char(string="Nombre", required=True)
    lines = fields.Many2one('dekam.line', string="Linea", required=True)
    item_module_ids = fields.One2many(
        'dekam.item.module',
        'project_id',
        string="Módulos",
        required=True,
    )
    total_accessorys = fields.Float(string="Costo Accesorios", compute="_compute_total_accessory")
    total_materials = fields.Float(string="Costo Materiales (sin madera)", compute="_compute_total_materials")

    resume_cut_ids = fields.One2many("dekam.resume.cut", compute="_compute_resume_cut", string="Resumen Cortes",
                                     store=False)
    resume_edge_ids = fields.One2many("dekam.resume.edge", compute="_compute_resume_edge", string="Resumen Canto",
                                      store=False)

    @api.depends('item_module_ids')
    def _compute_resume_cut(self):
        for project in self:
            project.resume_cut_ids = project.item_module_ids.module_id.mapped('resume_cut')

    @api.depends('item_module_ids')
    def _compute_resume_edge(self):
        for project in self:
            project.resume_edge_ids = project.item_module_ids.module_id.mapped('resume_edge')

    """
    total_hours = fields.Float(string="Horas Totales", compute="_compute_total_hours", store=True)
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_hours", store=True)

    sale_material_price = fields.Float(string="Costo Total", compute="_compute_sale_material_price", store=True)
    sale_acce_price = fields.Float(string="Costo Total", compute="_compute_sale_acce_price", store=True)
    sale_edge_price = fields.Float(string="Costo Total", compute="_compute_sale_edge_price", store=True)
    sale_workforce_price = fields.Float(string="Costo Total", compute="_compute_sale_workforce_price", store=True)

    sale_total_price = fields.Float(string="Costo Total", compute="_compute_sale_total_price", store=True)


    @api.onchange('lines')
    def _onchange_lines(self):
        if self.lines:
            # Actualiza el dominio del campo 'item_module_ids' para filtrar módulos según la línea seleccionada
            return {'domain': {'item_module_ids': [('module_id.line', '=', self.lines.id)]}}


    @api.depends('sale_material_price', 'sale_workforce_price', 'sale_acce_price', 'sale_edge_price')
    def _compute_sale_total_price(self):
        for record in self:
            record.sale_total_price = record.sale_material_price + record.sale_workforce_price + record.sale_acce_price + record.sale_edge_price

    """

    @api.depends('item_module_ids')
    def _compute_total_accessory(self):
        for record in self:
            total_acc = 0
            for module in record.item_module_ids:
                total_acc_module = 0
                if module.module_id.item_accessory_ids:
                    for acce in module.module_id.item_accessory_ids:
                        total_acc_module += (acce.accessory_id.cost_price * acce.quantity)
                if module.module_id.item_door_ids:
                    for door in module.module_id.item_door_ids:
                        total_acc_module += (door.door_id.total_accessorys * door.quantity)
                if module.module_id.item_box_ids:
                    for box in module.module_id.item_box_ids:
                        total_acc_module += (box.box.total_accessorys * box.quantity)
                total_acc += total_acc_module * module.quantity
            record.total_accessorys = total_acc


    @api.depends('item_module_ids')
    def _compute_total_materials(self):
        for record in self:
            total_materials = 0
            for module in record.item_module_ids:
                total_material_module = 0
                if module.module_id.total_cost_material:
                    total_material_module += module.module_id.total_cost_material
                if module.module_id.item_door_ids:
                    for door in module.module_id.item_door_ids:
                        total_material_module += (door.door_id.total_materials * door.quantity)
                if module.module_id.item_box_ids:
                    for box in module.module_id.item_box_ids:
                        total_material_module += (box.box.total_materials * box.quantity)
                total_materials += total_material_module * module.quantity
            record.total_materials = total_materials

    @api.onchange('item_module_ids')
    def _re_calculate_totals(self):
        for record in self:
            record._compute_total_accessory()