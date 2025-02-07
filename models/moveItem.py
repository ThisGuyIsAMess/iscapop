from odoo import models, fields

class MoveItem(models.TransientModel):
    _name = 'iscapop.move_item_model'
    _description = 'Transient Model to move items in bulk'

    name = fields.Char(string="Name")
    condition = fields.Selection([("new", "New"), ("good", "Good"), ("fair", "Fair"), ("poor", "Poor"), ("retired", "Retired")], string="Condition")
    category_id = fields.Many2one(string="Category", comodel_name="iscapop.category_model", ondelete="cascade")
    quantity = fields.Integer(string="Quantity to move", required=True)
    origin_id = fields.Many2one(string="Origin", comodel_name="iscapop.location_model", required=True, ondelete="cascade")
    destination_id = fields.Many2one(string="Destination", comodel_name="iscapop.location_model", required=True, ondelete="cascade")

    def action_move_item(self):
        #How to check if origin is the same as the one that triggered this action?
        items = None
        if self.name and self.condition and self.category_id:
            items = self.env['iscapop.item_model'].search([
                ('name', '=', self.name),
                ('condition', '=', self.condition),
                ('category_id', '=', self.category_id.id),
                ('location_id', '=', self.origin_id.id)
            ])
        if self.name and self.condition and not self.category_id:
            items = self.env['iscapop.item_model'].search([
                ('name', '=', self.name),
                ('condition', '=', self.condition),
                ('location_id', '=', self.origin_id.id)
            ])
        if self.name and not self.condition and not self.category_id:
            items = self.env['iscapop.item_model'].search([
                ('name', '=', self.name),
                ('location_id', '=', self.origin_id.id)
            ])
        if not self.name and self.condition and not self.category_id:
            items = self.env['iscapop.item_model'].search([
                ('condition', '=', self.condition),
                ('location_id', '=', self.origin_id.id)
            ])
        if not self.name and not self.condition and self.category_id:
            items = self.env['iscapop.item_model'].search([
                ('category_id', '=', self.category_id.id),
                ('location_id', '=', self.origin_id.id)
            ])
        if self.name and not self.condition and self.category_id:
            items = self.env['iscapop.item_model'].search([
                ('category_id', '=', self.category_id.id),
                ('location_id', '=', self.origin_id.id)
            ])
        if items != None:
            for i in range(self.quantity):
                items[i].location_id = self.destination_id.id