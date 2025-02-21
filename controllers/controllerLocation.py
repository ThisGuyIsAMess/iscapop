# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json

class controlerLocation(http.Controller):
    @http.route(['/iscapop/get_locations/','/iscapop/get_location/<int:locid>'], auth='public', type="http")
    def getLocations(self, locid=None, **kw):
        try:
            if locid == None:
                domain=[]
            else:
                domain=[("id","=",locid)]

            locations = http.request.env["iscapop.location_model"].sudo().search_read(domain,["name","description","item_ids","type"])
            data = {"status":200, "data": locations}
            return http.Response(json.dumps(data).encode("utf8"), mimetype="application/json")
        except Exception as e:
            data = {
                "status":404,
                "error":e.args
            }
            return data