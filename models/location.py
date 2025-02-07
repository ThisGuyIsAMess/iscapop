from odoo import models, fields

class LocationModel(models.Model):
    _name = 'iscapop.location_model'
    _description = 'Model for the Location'
    _order = 'name'
    _sql_constraints = [('iscapop_location_name_unique',
                         'UNIQUE (name)',
                         'There cannot be two locations with the same name!'),]

    name = fields.Char(string="Name", required=True)
    description = fields.Html(string="Description")
    item_ids = fields.One2many(string="Item Details", comodel_name="iscapop.item_model", inverse_name="location_id")
    type = fields.Selection([("class", "Class"), ("department", "Department"), ("storage", "Storage")], string="Type", default="class")