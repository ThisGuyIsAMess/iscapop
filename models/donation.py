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
    date = fields.Date(string="Date", readonly=True)
    donated_by = fields.Many2one(string="Donator", comodel_name="res.users")
    receiver = fields.Many2one(string="Reciever", comodel_name="res.users")
    reserved = fields.Boolean(string="Reserved", readonly=True, store=True)

    def returnToStorage(self):
        self.item_ids[0].donated = False
        self.unlink()

    def reserveItem(self):
        self.receiver = self.env.uid
        self.reserved = True

    def unreserveItem(self):
        self.reserved = False
        self.receiver = None
    
    def confirmDonation(self):
        if(self.reserved):
            item = self.item_ids[0]
            reserved_user = self.receiver.user_ids[0]
            env_with_reserved_user = self.env(user = reserved_user)
            env_with_reserved_user['iscapop.item_model'].create({
                'name': item.name,
                'description': item.description,
                'photo': item.photo,
                'documents': item.documents,
                'condition': item.condition,
                'category_id': item.category_id.id
            })
            item.unlink()
            self.unlink()