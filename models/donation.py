from odoo import models, fields

class DonationModel(models.Model):
    _name = 'iscapop.donation_model'
    _description = 'Model for a Donation'
    _order = 'date'

    item_ids = fields.Many2one(string="Item", comodel_name="iscapop.item_model", ondelete="cascade", readonly=True)
    name = fields.Char(string="Name", related='item_ids.name')
    photo = fields.Binary(string="Photo", related='item_ids.photo')
    condition = fields.Selection(string="Condition", related='item_ids.condition')
    category = fields.Char(string="Category", related='item_ids.category_id.name')
    date = fields.Date(string="Date")
    #Donator
    #Reciever
    #Reserved
    
    #Items can only be donated if they're in a storage location