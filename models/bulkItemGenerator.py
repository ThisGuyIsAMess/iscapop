from odoo import models, fields

class BulkItemGeneratorWizard(models.TransientModel):
    _name = 'iscapop.bulk_item_generator_model'
    _description = 'Transient Model to generate items in bulk'

    name = fields.Char(string="Name", required=True)
    description = fields.Html(string="Description")
    photo = fields.Binary(string="Photo", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    condition = fields.Selection([("new", "New"), ("good", "Good"), ("fair", "Fair"), ("poor", "Poor"), ("retired", "Retired")], string="Condition", default="fair")
    location_id = fields.Many2one(string="Location", comodel_name="iscapop.location_model", required=True, ondelete="cascade")
    category_id = fields.Many2one(string="Category", comodel_name="iscapop.category_model", required=True, ondelete="cascade")

    def action_generate_item(self):
        for _ in range(self.quantity):
            self.env['iscapop.item_model'].create({
                'name': self.name,
                'description': self.description,
                'photo': self.photo,
                'condition': self.condition,
                'location_id': self.location_id.id,
                'category_id': self.category_id.id
            })