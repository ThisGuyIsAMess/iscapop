from asyncio import exceptions
import datetime
from odoo import models, fields, api

class ItemModel(models.Model):
    _name = 'iscapop.item_model'
    _description = 'Model for the Item'
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    description = fields.Html(string="Description")
    photo = fields.Binary(string="Photo", required=True)
    documents = fields.Binary(string="Related Documents")
    condition = fields.Selection([("new", "New"), ("good", "Good"), ("fair", "Fair"), ("poor", "Poor"), ("retired", "Retired")], string="Condition", default="fair")
    location_id = fields.Many2one(string="Location", comodel_name="iscapop.location_model", required=True, ondelete="cascade")
    category_id = fields.Many2one(string="Category", comodel_name="iscapop.category_model", ondelete="cascade")
    donation_id = fields.One2many(string="Donated", comodel_name="iscapop.donation_model", inverse_name="item_ids", readonly=True)
    donated = fields.Boolean(string="Donated")
    #active = fields.Boolean(string="Active", readonly=True)

    def donateItem(self):
        if not self.donation_id:
            if self.location_id.type == "storage":
                self.env['iscapop.donation_model'].create({
                    'item_ids': self.id,
                    'name': self.name,
                    'photo': self.photo,
                    'condition': self.condition,
                    'category': self.category_id.name,
                    'date': datetime.datetime.now(),
                    'donator': self.env.user.id
                })
                self.donated=True
            else:
                raise exceptions.UserError("The item must be in storage to be donated!")
        else:
            raise exceptions.UserError("This item has already been donated!")