from reportlab.lib.pagesizes import elevenSeventeen

from odoo import models, fields, api

class Module(models.Model):
    _name = 'dekam.module'
    _description = 'Modulo'

    name = fields.Char(string="Nombre", required=True)
    line = fields.Many2one('dekam.line' , string="Linea", required=True)
    wood = fields.Many2one('dekam.material' , string="Madera Caja", required=True)
    edge = fields.Many2one('dekam.edge', string="Canto de Caja", required=True)
    item_material_ids = fields.One2many('dekam.item.material', 'module_id', string="Materiales", required=True)
    total_cost_material = fields.Float(string="Costo Materiales", compute="_compute_total_cost_material", store=True)
    complete_top = fields.Boolean(string="Tapa Superior?")
    strip_width = fields.Float(string="Ancho de Listones (mm)", required=True)
    strip_quantity = fields.Integer(string="Cantidad de Listones", required=True)
    rack_quantity = fields.Integer(string="Cantidad de Estantes", required=True)
    high = fields.Float (string="Alto", required=True)
    width = fields.Float (string="Ancho", required=True)
    depth = fields.Float (string="Profundidad", required=True)
    box_work_hours = fields.Float(string="Horas de Fabricación (Caja)", required=True)
    is_door_inside = fields.Boolean(string="Puerta Interior?")
    orientation = fields.Selection([
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical')
    ], string="Orientación", default='vertical')

    grain = fields.Selection([
        ('no', 'No'),
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical')
    ], string="Veta", default='no', required=True)
    item_door_ids = fields.One2many('dekam.item.door', 'module_id', string="Puertas")
    total_cost_door = fields.Float(string="Costo Total de la Puerta", compute="_compute_total_cost_door", store=True)
    total_hours_door = fields.Float(string="Horas de Trabajo", compute="_compute_total_hours_door", store=True)
    is_box_inside = fields.Boolean(string="Cajón Interior?")
    item_box_ids = fields.One2many('dekam.item.box', 'module_id', string="Cajones")
    total_cost_box = fields.Float(string="Costo Cajones (Sin Madera)", compute="_compute_total_cost_box", store=True)
    total_hours_box = fields.Float(string="Horas de Trabajo", compute="_compute_total_hours_box", store=True)
    front_wood = fields.Many2one('dekam.material', string="Madera Frente")
    item_accessory_ids = fields.One2many('dekam.item.accessory', 'module_id', string="Accesorios")
    total_accessorys = fields.Float(string="Costo Accesorios", compute="_compute_total_accessory", store=True)
    total_hours_acce = fields.Float(string="Horas de Trabajo", compute="_compute_total_hours_acc", store=True)
    total_workforce_acce = fields.Float(string="Costo ", compute="_compute_total_workforce", store=True)
    cuts = fields.One2many('dekam.cut', 'module_id' , string="Cortes")
    resume_cut = fields.One2many('dekam.resume.cut', 'module_id' , string="Resumen Cortes")
    resume_edge = fields.One2many('dekam.resume.edge', 'module_id', string="Resumen Canto")
    total_cost = fields.Float(string="Costo Total del Módulo", compute="_compute_total_cost", store=True)
    total_hours = fields.Float(string="Horas Totales de Trabajo", compute="_compute_total_hours", store=True)


    @api.depends('item_door_ids.total_cost')
    def _compute_total_cost_door(self):
        for record in self:
            record.total_cost_door = sum(item.total_cost for item in record.item_door_ids)

    @api.depends('item_material_ids.total_cost')
    def _compute_total_cost_material(self):
        for record in self:
            record.total_cost_material = sum(item.total_cost for item in record.item_material_ids)

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
            record.total_accessorys = sum(item.total_cost for item in record.item_accessory_ids)

    @api.depends('item_accessory_ids.total_hours')
    def _compute_total_hours_acc(self):
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
            all_cuts.extend(record._generate_door_cuts())
            all_cuts.extend(record._generate_drawer_cuts())
            all_cuts.extend(record._generate_background_cuts())


            # Crear registros de dekam.cut y relacionarlos con la instancia actual
            for cut_vals in all_cuts:
                cut_vals['module_id'] = record.id  # Relacionar con el módulo actual
                self.env['dekam.cut'].create(cut_vals)

            record._generate_resume()

    def _generate_box_cuts(self):
        """
        Genera los cortes para la caja del módulo.
        """
        cuts = []
        for record in self:
            if record.high and record.width and record.depth:
                cuts.append({
                    'name': f' Caja Lat - {record.name}',
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
                    'name': f'Caja Piso - {record.name}',
                    'quantity': 1,
                    'wood': record.wood.id,
                    'length': record.width - (record.wood.thickness * 2),
                    'width': record.depth,
                    'edge': record.edge.id,
                    'left': False,
                    'right': False,
                    'top': True,
                    'bottom': True,
                })
                if record.complete_top:
                    cuts.append({
                        'name': f'Caja Techo - {record.name}',
                        'quantity': 1,
                        'wood': record.wood.id,
                        'length': record.width - (record.wood.thickness * 2),
                        'width': record.depth,
                        'edge': record.edge.id,
                        'left': False,
                        'right': False,
                        'top': True,
                        'bottom': True,
                    })
                cuts.append({
                    'name': f'Caja Liston - {record.name}',
                    'quantity': record.strip_quantity,
                    'wood': record.wood.id,
                    'length': record.width - (record.wood.thickness * 2),
                    'width': record.strip_width,
                    'edge': record.edge.id,
                    'left': False,
                    'right': False,
                    'top': True,
                    'bottom': True,
                })
                if record.rack_quantity > 0:
                    cuts.append({
                        'name': f'Caja Est. - {record.name}',
                        'quantity': record.rack_quantity,
                        'wood': record.wood.id,
                        'length': record.width - (record.wood.thickness * 2),
                        'width': record.depth - 40,
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
                    box_quantity = (sum(item.quantity for item in self.item_box_ids))
                    # Frente Visto de cajones, Calculados todos de la misma medida teniendo en cuenta la cantidad de cajones
                    # Si el cajon es interno
                    if record.is_box_inside:
                        cuts.append({
                            'name': f'Cajon Frente V - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': record.front_wood.id,
                            'length': record.width - (record.wood.thickness * 2) - (drawer.box.lateral_space * 2) - (drawer.box.edge_front.thickness * 2),
                            'width': (record.high - (record.wood.thickness * 2) - (drawer.box.top_space * 2)
                                      - (drawer.box.between_box_space * (box_quantity - 1))
                                      - (drawer.box.edge_front.thickness * 2)) / box_quantity
                                      if not drawer.box.with_profile  # Usamos 'not' para mejor claridad
                                      else (record.high - (record.wood.thickness * 2) - drawer.box.top_space
                                            - (drawer.box.between_box_space * (box_quantity - 1))
                                            - (drawer.box.profile_size * box_quantity)
                                            - drawer.box.edge_front.thickness) / box_quantity,
                            'edge': drawer.box.edge_front.id,
                            'left': True,
                            'right': True,
                            'top': True if not drawer.box.with_profile else False,
                            'bottom': True,
                            'grain': record.grain,
                        })
                    else:
                        # Si el Cajon es Externo
                        cuts.append({
                            'name': f'Cajon Frente V - {drawer.box.name}',
                            'quantity': 1 * drawer.quantity,
                            'wood': record.front_wood.id,
                            'length': record.width - (drawer.box.lateral_space * 2) - (drawer.box.edge_front.thickness * 2),
                            'width':  (record.high - drawer.box.top_space
                                      - drawer.box.between_box_space * (box_quantity - 1)
                                      - (drawer.box.edge_front.thickness * 2)) / box_quantity
                                      if not drawer.box.with_profile  # Usamos 'not' para mejor claridad
                                      else (record.high - drawer.box.top_space
                                            - (drawer.box.between_box_space * (box_quantity - 1))
                                            - drawer.box.profile_size * box_quantity
                                            - drawer.box.edge_front.thickness) / box_quantity,
                            'edge': drawer.box.edge_front.id,
                            'left': True,
                            'right': True,
                            'top': True if not drawer.box.with_profile else False,
                            'bottom': True,
                            'grain': record.grain,
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
                            'name': f'Cajon F y CF Int - {drawer.box.name}',
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
                            'name': f'Cajon CF - {drawer.box.name}',
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

    def _generate_door_cuts(self):

        for record in self:
            cuts = []
            if self.item_door_ids:
                if record.orientation == 'vertical':
                    for door in self.item_door_ids:
                        door_quantity = sum(item.quantity for item in self.item_door_ids)
                        if record.is_door_inside:
                            cuts.append({
                                'name': f'Puerta {door.door_id.name}',
                                'quantity': 1 * door.quantity,
                                'wood': record.front_wood.id,
                                'length': record.high - (record.wood.thickness * 2) - (
                                            door.door_id.edge.thickness * 2) - door.door_id.light_vertical,
                                'width': (record.width - (record.wood.thickness * 2) - (
                                            door.door_id.edge.thickness * 2) - door.door_id.light_horizontal) / door_quantity,
                                'edge': door.door_id.edge.id,
                                'left': True,
                                'right': True,
                                'top': True,
                                'bottom': True,
                                'grain': record.grain,
                            })
                        else:
                            cuts.append({
                                'name': f'Puerta {door.door_id.name}',
                                'quantity': 1 * door.quantity,
                                'wood': record.front_wood.id,
                                'length': record.high - (door.door_id.edge.thickness * 2) - door.door_id.light_vertical,
                                'width': (record.width - (
                                            door.door_id.edge.thickness * 2) - door.door_id.light_horizontal) / door_quantity,
                                'edge': door.door_id.edge.id,
                                'left': True,
                                'right': True,
                                'top': True,
                                'bottom': True,
                                'grain': record.grain,
                            })
                else:
                    for door in self.item_door_ids:
                        door_quantity = sum(item.quantity for item in self.item_door_ids)
                        if record.is_door_inside:
                            cuts.append({
                                'name': f'Puerta {door.door_id.name}',
                                'quantity': 1 * door.quantity,
                                'wood': record.front_wood.id,
                                'length': (record.width - (record.wood.thickness * 2) - (door.door_id.edge.thickness * 2) - door.door_id.light_horizontal) / door_quantity,
                                'width': record.high - (record.wood.thickness * 2) - (door.door_id.edge.thickness * 2) - door.door_id.light_vertical,
                                'edge': door.door_id.edge.id,
                                'left': True,
                                'right': True,
                                'top': True,
                                'bottom': True,
                                'grain': record.grain,
                            })
                        else:
                            cuts.append({
                                'name': f'Puerta {door.door_id.name}',
                                'quantity': 1 * door.quantity,
                                'wood': record.front_wood.id,
                                'length': (record.width - (door.door_id.edge.thickness * 2) - door.door_id.light_horizontal) / door_quantity,
                                'width': record.high - (door.door_id.edge.thickness * 2) - door.door_id.light_vertical,
                                'edge': door.door_id.edge.id,
                                'left': True,
                                'right': True,
                                'top': True,
                                'bottom': True,
                                'grain': record.grain,
                            })
            return cuts

    def _generate_background_cuts(self):

        for record in self:
            cuts = []
            if record.line.background.background_type == "Ranurado":
                cuts.append({
                    'name': f'Fondo - {record.line.background.background_type}',
                    'quantity': 1,
                    'wood': record.line.background.wood.id,
                    'length': record.high - 10 ,
                    'width': record.width - (10 * 2),
                })
            elif record.line.background.background_type == "Engrampado":
                cuts.append({
                    'name': f'Fondo - {record.line.background.background_type}',
                    'quantity': 1,
                    'wood': record.line.background.wood.id,
                    'length': record.high,
                    'width': record.width,
                })
            elif record.line.background.background_type == "MDF Entarugado":
                cuts.append({
                    'name': f'Fondo - {record.line.background.background_type}',
                    'quantity': 1,
                    'wood': record.line.background.wood.id,
                    'length': record.high - (record.wood.thickness * 2),
                    'width': record.width - (record.wood.thickness * 2),
                })
            return cuts

    def _generate_resume(self):
        for record in self:
            # Filtrar los cortes solo del módulo actual
            cuts = record.cuts

            # Limpiar registros previos de resumen
            if record.resume_cut:
                record.resume_cut.unlink()
            if record.resume_edge:
                record.resume_edge.unlink()

            # Obtener resumen de cortes por material SOLO para el módulo actual
            cuts_resume = self.env['dekam.cut'].read_group(
                [('module_id', '=', record.id), ('wood', '!=', False)],  # Filtrar por módulo actual
                ['wood', 'squareMeters:sum'],
                ['wood']
            )

            # Obtener resumen de cantos por material SOLO para el módulo actual
            edges_resume = self.env['dekam.cut'].read_group(
                [('module_id', '=', record.id), ('wood', '!=', False)],  # Filtrar por módulo actual
                ['edge', 'edgeMeters:sum'],
                ['edge']
            )

            # Crear instancias para los cortes
            for cut in cuts_resume:
                if cut['wood']:  # Verificar si hay material
                    self.env['dekam.resume.cut'].create({
                        'module_id': record.id,
                        'material_id': cut['wood'][0],  # ID del material
                        'total_m2': cut['squareMeters'],
                    })

            # Crear instancias para los cantos
            for cut in edges_resume:
                if cut['edge']:  # Verificar si hay canto
                    self.env['dekam.resume.edge'].create({
                        'module_id': record.id,
                        'edge_id': cut['edge'][0],
                        'total_mt': cut['edgeMeters'],  # Convertir mm a metros
                    })

    @api.depends('box_work_hours', 'total_hours_door', 'total_hours_box', 'total_hours_acce')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = record.box_work_hours + record.total_hours_door + record.total_hours_box + record.total_hours_acce

    @api.depends('total_hours','total_cost_material', 'total_cost_door', 'total_cost_box', 'total_accessorys', 'resume_cut', 'resume_edge')
    def _compute_total_cost(self):
        for record in self:
            workforce = self.env['dekam.workforce'].search([], limit=1)
            total_wood = sum(item.material_cost for item in record.resume_cut)
            total_edge = sum(item.edge_cost for item in record.resume_edge)
            record.total_cost = (workforce.cost_per_hour * record.total_hours) + total_wood + total_edge

