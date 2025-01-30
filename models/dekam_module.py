from odoo import models, fields, api

class Module(models.Model):
    _name = 'dekam.module'
    _description = 'Modulo'

    name = fields.Char(string="Nombre")
    line = fields.Many2one('dekam.line' , string="Linea")
    wood = fields.Many2one('dekam.material' , string="Madera Caja")
    edge = fields.Many2one('dekam.edge', string="Canto de Caja")
    item_material_ids = fields.One2many('dekam.item.material', 'module_id', string="Materiales")
    complete_top = fields.Boolean(string="Tapa Superior?")
    strip_width = fields.Float(string="Ancho de Listones (mm)")
    strip_quantity = fields.Integer(string="Cantidad de Listones")
    rack_quantity = fields.Integer(string="Cantidad de Estantes")
    high = fields.Float (string="Alto")
    width = fields.Float (string="Ancho")
    depth = fields.Float (string="Profundidad")
    box_work_hours = fields.Float(string="Horas de Fabricación (Caja)")
    item_door_ids = fields.One2many('dekam.item.door', 'module_id', string="Puertas")
    total_cost_door = fields.Float(string="Costo Total de la Puerta", compute="_compute_total_cost_door", store=True)
    total_hours_door = fields.Float(string="Horas de Trabajo", compute="_compute_total_hours_door", store=True)
    item_box_ids = fields.One2many('dekam.item.box', 'module_id', string="Cajones")
    total_cost_box = fields.Float(string="Costo Cajones (Sin Madera)", compute="_compute_total_cost_box", store=True)
    total_hours_box = fields.Float(string="Horas de Trabajo", compute="_compute_total_hours_box", store=True)
    front_wood = fields.Many2one('dekam.material', string="Madera Frente")
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'module_id', string="Accesorios")
    total_accessorys = fields.Float(string="Costo Accesorios", compute="_compute_total_accessory", store=True)
    total_hours_acce = fields.Float(string="Horas de Trabajo", compute="_compute_total_hours", store=True)
    total_workforce_acce = fields.Float(string="Costo ", compute="_compute_total_workforce", store=True)
    total_cost = fields.Float(string="Costo Total del Módulo", compute="_compute_total_cost", store=True)
    cuts = fields.One2many('dekam.cut', 'module_id' , string="Cortes")


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

    @api.depends('item_box_ids.total_hours')
    def _compute_total_hours_box(self):
        for record in self:
            record.total_hours_box = sum(item.total_hours for item in record.item_box_ids)

    @api.depends('item_door_ids.total_hours')
    def _compute_total_hours_door(self):
        for record in self:
            record.total_hours_door = sum(item.total_hours for item in record.item_door_ids)

    @api.depends('item_accessory_ids.total_cost', 'total_workforce_acce')
    def _compute_total_accessory(self):
        for record in self:
            record.total_accessorys = sum(item.total_cost for item in record.item_accessory_ids) + record.total_workforce_acce

    @api.depends('item_accessory_ids.total_hours')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours_acce = sum(item.total_hours for item in record.item_accessory_ids)


    @api.depends('total_hours_acce')
    def _compute_total_workforce(self):
        for record in self:
            workforce = self.env['dekam.workforce'].search([], limit=1)
            cost_per_hour = workforce.cost_per_hour
            record.total_workforce_acce = (record.total_hours_acce * cost_per_hour)


    def create_cut_list(self):
        """
        Método principal para crear cortes, llama a métodos específicos.
        """
        for record in self:
            # Eliminar solo los cortes asociados al módulo actual
            record.cuts.unlink()

            all_cuts = []
            # Llamar a métodos específicos para cada tipo de corte
            all_cuts.extend(record._generate_box_cuts())
            all_cuts.extend(record._generate_drawer_cuts())
            """
            all_cuts.extend(record._generate_door_cuts())
            """

            # Crear registros de dekam.cut y relacionarlos con la instancia actual
            for cut_vals in all_cuts:
                cut_vals['module_id'] = record.id  # Relacionar con el módulo actual
                self.env['dekam.cut'].create(cut_vals)

    def _generate_box_cuts(self):
        """
        Genera los cortes para la caja del módulo.
        """
        cuts = []
        for record in self:
            if record.high and record.width and record.depth:
                cuts.append({
                    'name': f'Lateral - {record.name}',
                    'quantity': 2,
                    'wood': record.wood.id,
                    'length': record.high,
                    'width': record.depth,
                    'edge': record.edge.id,
                    'left': True,
                    'right': True,
                    'top': True,
                    'bottom': True,
                })
                cuts.append({
                    'name': f'Piso - {record.name}',
                    'quantity': 1,
                    'wood': record.wood.id,
                    'length': record.width - 36,
                    'width': record.depth,
                    'edge': record.edge.id,
                    'left': False,
                    'right': False,
                    'top': True,
                    'bottom': True,
                })
                if record.complete_top:
                    cuts.append({
                        'name': f'Techo - {record.name}',
                        'quantity': 1,
                        'wood': record.wood.id,
                        'length': record.width - 36,
                        'width': record.depth,
                        'edge': record.edge.id,
                        'left': False,
                        'right': False,
                        'top': True,
                        'bottom': True,
                    })
                cuts.append({
                    'name': f'Liston - {record.name}',
                    'quantity': record.strip_quantity,
                    'wood': record.wood.id,
                    'length': record.width - 36,
                    'width': record.strip_width,
                    'edge': record.edge.id,
                    'left': False,
                    'right': False,
                    'top': True,
                    'bottom': True,
                })
                if record.rack_quantity > 0:
                    cuts.append({
                        'name': f'Estante - {record.name}',
                        'quantity': record.rack_quantity,
                        'wood': record.wood.id,
                        'length': record.width - 36,
                        'width': record.depth - 20,
                        'edge': record.edge.id,
                        'left': False,
                        'right': False,
                        'top': True,
                        'bottom': True,
                    })
        return cuts


    def _generate_drawer_cuts(self):
        cuts = []
        for record in self:
            if self.item_box_ids:
                for drawer in self.item_box_ids:
                    # Frente Visto de cajones, Calculados todos de la misma medida teniendo en cuenta la cantidad de cajones
                    # Si el cajon es interno
                    if drawer.box.is_inside:
                        cuts.append({
                            'name': f'Cajon Frente V - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': record.front_wood.id,
                            'length': record.width - (record.wood.thickness * 2) - (drawer.box.lateral_space * 2),
                            'width': record.high - (record.wood.thickness * 2) - (drawer.box.top_space * 2)
                                      - (drawer.box.between_box_space * ((sum(item.quantity for item in self.item_box_ids)) - 1))
                                      if not drawer.box.with_profile  # Usamos 'not' para mejor claridad
                                      else record.high - (record.wood.thickness * 2) - drawer.box.top_space
                                            - (drawer.box.between_box_space * ((sum(item.quantity for item in self.item_box_ids)) - 1))
                                            - (drawer.box.profile_size * (sum(item.quantity for item in self.item_box_ids))),
                            'edge': drawer.box.edge_front.id,
                            'left': True,
                            'right': True,
                            'top': True,
                            'bottom': True,
                        })
                    else:
                        # Si el Cajon es Externo
                        cuts.append({
                            'name': f'Cajon Frente V - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': record.front_wood.id,
                            'length': record.width - (drawer.box.lateral_space * 2),
                            'width': (record.high - drawer.box.top_space
                                      - (drawer.box.between_box_space * ((sum(item.quantity for item in self.item_box_ids)) - 1))
                                      if not drawer.box.with_profile  # Usamos 'not' para mejor claridad
                                      else (record.high - drawer.top_space
                                            - (drawer.box.between_box_space * ((sum(item.quantity for item in self.item_box_ids)) - 1))
                                            - (drawer.box.profile_size * len(self.item_box_ids)))),
                            'edge': drawer.box.edge_front.id,
                            'left': True,
                            'right': True,
                            'top': True,
                            'bottom': True,
                        })
                    # Cortes Especiales si la totalidad del cajon se hace en MDF
                    if drawer.box.is_lateral_wood:
                        # Laterales
                        cuts.append({
                            'name': f'Cajon Lateral - {drawer.box.name}',
                            'quantity': 2 * drawer.quantity,
                            'wood': drawer.box.lateral_wood.id,
                            'length': drawer.box.depth,
                            'width': drawer.box.high,
                            'edge': drawer.box.edge_box.id,
                            'left': False,
                            'right': False,
                            'top': True,
                            'bottom': True,
                        })
                        # Piso (Puede ser Ranurado o Entarugado)
                        cuts.append({
                            'name': f'Cajon Piso - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': drawer.box.floor_wood.id,
                            'length': record.width - (drawer.box.lateral_wood.thickness * 2) - drawer.box.slide_space
                                        if drawer.box.type_union_floor == "doweled"
                                        else record.width - (drawer.box.lateral_wood.thickness * 2) - drawer.box.slide_space + 12,
                            'width': drawer.box.depth - (drawer.box.lateral_wood.thickness * 2) - 1
                                        if drawer.box.type_union_floor == "doweled"
                                        else drawer.box.depth - (drawer.box.lateral_wood.thickness * 2) + 12,
                            'edge': drawer.box.edge_box.id,
                            'left': False,
                            'right': False,
                            'top': False,
                            'bottom': False,
                        })
                        # Frente y Contra frente
                        cuts.append({
                            'name': f'Fr y Contra Int - {drawer.box.name}',
                            'quantity': 2 * drawer.quantity,
                            'wood': drawer.box.lateral_wood.id,
                            'length': record.width - (drawer.box.lateral_wood.thickness * 2) - drawer.box.slide_space,
                            'width': drawer.box.high,
                            'edge': drawer.box.edge_box.id,
                            'left': False,
                            'right': False,
                            'top': True,
                            'bottom': True,
                        })
                    else:
                        # Piso (Cajones con laterales de acero)
                        cuts.append({
                            'name': f'Cajon Piso - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': drawer.box.floor_wood.id,
                            'length': record.width - (record.wood.thickness * 2) - drawer.box.floor_length,
                            'width': drawer.box.depth - drawer.box.floor_depth,
                            'edge': drawer.box.edge_box.id,
                            'left': False,
                            'right': False,
                            'top': True,
                            'bottom': True,
                        })
                        # Contra frente (Con laterales de acero)
                        cuts.append({
                            'name': f'Contra Fr - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': drawer.box.floor_wood.id,
                            'length': record.width - (drawer.box.lateral_wood.thickness * 2) - drawer.box.back_facade_length,
                            'width': drawer.box.high,
                            'edge': drawer.box.edge_box.id,
                            'left': False,
                            'right': False,
                            'top': True,
                            'bottom': True,
                        })
        return cuts

    """

    def _generate_door_cuts(self):

        cuts = []
        if self.item_door_ids:
            for door in self.item_door_ids:
                cuts.append({
                    'name': f'Puerta {door.id}',
                    'quantity': 1,
                    'wood': door.wood.id,
                    'length': door.high,
                    'width': door.width,
                })
        return cuts
    
    """