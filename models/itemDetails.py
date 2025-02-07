from odoo import models, fields, api, exceptions

class ItemDetailsModel(models.Model):
    _name = 'iscapop.item_details_model'
    _description = 'Model for the Item Details'
    _order = 'item_id'

    name = fields.Char(related="item_id.name")
    photo = fields.Image(related="item_id.photo")
    item_id = fields.Many2one(string="Item", comodel_name="iscapop.item_model", required=True, ondelete="cascade")
    location_id = fields.Many2one(string="Location", comodel_name="iscapop.location_model", required=True, ondelete="cascade")
    documents = fields.Binary(string="Related Documents")
    condition = fields.Selection([("new", "New"), ("good", "Good"), ("fair", "Fair"), ("poor", "Poor"), ("retired", "Retired")], string="Condition", default="fair")

    