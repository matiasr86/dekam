from odoo import models, fields, api

class Material(models.Model):
    _name = 'dekam.material'
    _description = 'Material'

    name = fields.Char(string="Nombre")
    costPrice = fields.Float(string="Precio de Costo")
    urls = fields.Many2many('dekam.url', 'material_id', string="Url Proveedores")
    isWood = fields.Boolean(string="Es Madera?")
    length = fields.Float(string="Largo")
    width = fields.Float (string="Ancho")
    thickness = fields.Float (string= "Espesor")
    squareMetersPrice = fields.Float(string="Precio x Mts2", compute="_compute_square_meters_price", store=True)

    @api.depends('length', 'width', 'costPrice')
    def _compute_square_meters_price(self):
        for record in self:
            # Convertir largo y ancho de mm a metros
            length_in_meters = record.length / 1000
            width_in_meters = record.width / 1000

            # Calcular el área en metros cuadrados
            area_in_square_meters = length_in_meters * width_in_meters

            # Calcular el precio por metro cuadrado
            if area_in_square_meters > 0:
                record.squareMetersPrice = record.costPrice / area_in_square_meters
            else:
                record.squareMetersPrice = 0



