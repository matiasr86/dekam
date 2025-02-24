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
    total_woods = fields.Float(string="Costo Materiales (Madera)", compute="_compute_total_woods")
    total_edges = fields.Float(string="Costo Canto", compute="_compute_total_edges")
    total_hours = fields.Float(string="Horas de Trabajo", compute="_compute_total_hs")
    total_cost_hours = fields.Float(string="Costo Mano de Obra", compute="_compute_total_hs_cost")
    total_cost = fields.Float(string="Costo Total", compute="_compute_total_cost")

    total_sale_accessorys = fields.Float(string="PV Accesorios", compute="_compute_total_sale_accessory")
    total_sale_materials = fields.Float(string="PV Material", compute="_compute_total_sale_materials")
    total_sale_edges = fields.Float(string="PV Canto", compute="_compute_total_sale_edges")
    total_sale_work_hs = fields.Float(string="PV Mano de Obra", compute="_compute_total_hs_sale")
    total_sale = fields.Float(string="Precio de Venta", compute="_compute_total_sale")


    resume_cut_ids = fields.One2many(
    "dekam.project.resume.cut", "project_id",
    string="Resumen Cortes", ondelete="cascade")
    resume_edge_ids = fields.One2many(
    "dekam.project.resume.edge", "project_id",
    string="Resumen Canto", ondelete="cascade")


    def compute_project_cuts(self):
        for project in self:
            # Eliminar cortes previos correctamente
            self.env['dekam.project.cut'].search([('project_id', '=', project.id)]).unlink()

            # Crear nuevas instancias de cortes en la base de datos
            cuts_to_create = []
            for item in project.item_module_ids:
                if item.module_id:
                    for cut in item.module_id.cuts:
                        cuts_to_create.append({
                            'name': cut.name,
                            'quantity': cut.quantity * item.quantity,
                            'wood': cut.wood.id if cut.wood else False,
                            'length': cut.length,
                            'width': cut.width,
                            'edge': cut.edge.id if cut.edge else False,
                            'left': cut.left,
                            'right': cut.right,
                            'top': cut.top,
                            'bottom': cut.bottom,
                            'module_id': item.module_id.id,
                            'project_id': project.id
                        })

            # Crear los registros de `dekam.project.cut` en la base de datos
            if cuts_to_create:
                self.env['dekam.project.cut'].create(cuts_to_create)

    def _compute_total_sale_accessory(self):
        for record in self:
            line = self.env['dekam.line'].search([('id', '=', self.lines.id)], limit=1)
            record.total_sale_accessorys = record.total_accessorys * (1 + (line.accessoriesMargin / 100))


    def _compute_total_sale_materials(self):
        for record in self:
            line = self.env['dekam.line'].search([('id', '=', self.lines.id)], limit=1)
            record.total_sale_materials = (record.total_materials + record.total_woods) * (1 +(line.materialMargin / 100))

    def _compute_total_sale_edges(self):
        for record in self:
            line = self.env['dekam.line'].search([('id', '=', self.lines.id)], limit=1)
            record.total_sale_edges = record.total_edges * (1 + (line.edgeMargin / 100))

    def _compute_total_hs_sale(self):
        for record in self:
            line = self.env['dekam.line'].search([('id', '=', self.lines.id)], limit=1)
            record.total_sale_work_hs = record.total_cost_hours * (1 + (line.workForceMargin / 100))

    def _compute_total_sale(self):
        for record in self:
            record.total_sale = record.total_sale_accessorys + record.total_sale_materials + record.total_sale_edges + record.total_sale_work_hs

    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.total_cost_hours + record.total_woods + record.total_edges + record.total_accessorys + record.total_materials

    def _compute_total_hs(self):
        for record in self:
            record.total_hours = sum(module.total_hours for module in record.item_module_ids)

    def _compute_total_hs_cost(self):
        for record in self:
            workforce = self.env['dekam.workforce'].search([], limit=1)
            record.total_cost_hours = record.total_hours * workforce.cost_per_hour

    def _compute_total_woods(self):
        for record in self:
            total = self.env['dekam.project.resume.cut'].search([('project_id', '=', record.id)]).mapped(
                'material_cost')
            record.total_woods = sum(total)


    def _compute_total_edges(self):
        for record in self:
            total = self.env['dekam.project.resume.edge'].search([('project_id', '=', record.id)]).mapped(
                'edge_cost')
            record.total_edges = sum(total)


    def _compute_total_accessory(self):
        for record in self:
            total_acc = 0
            for module in record.item_module_ids:
                total_acc_module = sum(acce.accessory_id.cost_price * acce.quantity for acce in module.module_id.item_accessory_ids)
                total_acc_module += sum(door.door_id.total_accessorys * door.quantity for door in module.module_id.item_door_ids)
                total_acc_module += sum(box.box.total_accessorys * box.quantity for box in module.module_id.item_box_ids)
                total_acc += total_acc_module * module.quantity
            record.total_accessorys = total_acc


    def _compute_total_materials(self):
        for record in self:
            total_materials = sum(
                (module.module_id.total_cost_material or 0) * module.quantity
                for module in record.item_module_ids
            )
            total_materials += sum(
                (door.door_id.total_materials * door.quantity) for module in record.item_module_ids for door in module.module_id.item_door_ids
            )
            total_materials += sum(
                (box.box.total_materials * box.quantity) for module in record.item_module_ids for box in module.module_id.item_box_ids
            )
            record.total_materials = total_materials

    def _generate_project_resume(self):
        for project in self:
            # Eliminar registros previos
            project.resume_cut_ids.unlink()
            project.resume_edge_ids.unlink()

            cut_records = []
            edge_records = []

            # Obtener cortes por material
            cut_data = {}
            for module in project.item_module_ids:
                for cut in module.module_id.resume_cut:
                    material_id = cut.material_id.id
                    total_m2 = cut.total_m2 * module.quantity  # Ajuste: multiplicar por la cantidad de módulos

                    if material_id in cut_data:
                        cut_data[material_id] += total_m2
                    else:
                        cut_data[material_id] = total_m2

            for material_id, total_m2 in cut_data.items():
                cut_records.append((0, 0, {
                    'project_id': project.id,
                    'material_id': material_id,
                    'total_m2': total_m2,
                }))

            # Obtener cantos por tipo
            edge_data = {}
            for module in project.item_module_ids:
                for edge in module.module_id.resume_edge:
                    edge_id = edge.edge_id.id
                    total_mt = edge.total_mt * module.quantity  # Ajuste: multiplicar por la cantidad de módulos

                    if edge_id in edge_data:
                        edge_data[edge_id] += total_mt
                    else:
                        edge_data[edge_id] = total_mt

            for edge_id, total_mt in edge_data.items():
                edge_records.append((0, 0, {
                    'project_id': project.id,
                    'edge_id': edge_id,
                    'total_mt': total_mt,
                }))

            project.write({
                'resume_cut_ids': cut_records,
                'resume_edge_ids': edge_records,
            })

    def generate_result(self):
        for record in self:
            record._generate_project_resume()
            record._compute_total_woods()
            record._compute_total_edges()
            record._compute_total_accessory()
            record._compute_total_materials()
            record._compute_total_hs()
            record._compute_total_hs_cost()
            record.compute_project_cuts()




class ProjectResumeCut(models.Model):
    _name = 'dekam.project.resume.cut'
    _description = 'Resumen de Cortes por Proyecto'

    project_id = fields.Many2one('dekam.project', string="Proyecto", ondelete="cascade")
    material_id = fields.Many2one('dekam.material', string="Material", required=True)
    total_m2 = fields.Float(string="Total m²")
    material_cost = fields.Float(string="$ Total", compute="_compute_material_cost")
    wood_quantity = fields.Float(string="Placas", compute="_compute_wood_quantity")

    @api.depends('total_m2', 'material_id')
    def _compute_material_cost(self):
        for record in self:
            record.material_cost = (record.total_m2 * record.material_id.squareMetersPrice) * 1.10
            # 1.10 es el 10% adicional que representa el desperdicio

    @api.depends('total_m2', 'material_id')
    def _compute_wood_quantity(self):
        for record in self:
            record.wood_quantity = round(
                (record.total_m2 * 1.10) / ((record.material_id.length * record.material_id.width) / 1000000), 2)
            # 1.10 es el 10% adicional que representa el desperdicio

class ProjectResumeEdge(models.Model):
    _name = 'dekam.project.resume.edge'
    _description = 'Resumen de Cantos por Proyecto'

    project_id = fields.Many2one('dekam.project', string="Proyecto", ondelete="cascade")
    edge_id = fields.Many2one('dekam.edge', string="Canto", required=True)
    total_mt = fields.Float(string="Total m")
    edge_cost = fields.Float(string="$ Total", compute="_compute_edge_cost")

    @api.depends('total_mt', 'edge_id')
    def _compute_edge_cost(self):
        for record in self:
            record.edge_cost = (record.total_mt * record.edge_id.cost_price) * 1.10
            # 1.10 es el 10% adicional que representa el desperdicio
