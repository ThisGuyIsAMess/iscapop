# -*- coding: utf-8 -*-
import datetime
from odoo import http
from odoo.http import json

class controlerDonation(http.Controller):
    @http.route(['/iscapop/get_donations/','/iscapop/get_donation/<int:donid>'], auth='public', type="http")
    def getDonations(self, donid=None, **kw):
        try:
            if donid == None:
                domain=[]
            else:
                domain=[("id","=",donid)]
            donations = http.request.env["iscapop.donation_model"].sudo().search_read(domain,["item_ids", "name", "condition", "category", "date", "donated_by", "receiver", "reserved"])
            for donation in donations:
                for name, value in donation.items():
                    if isinstance(value, datetime.date):
                        donation[name] = value.strftime('%Y-%m-%d')
            data = {"status":200, "data": donations}
            return http.Response(json.dumps(data).encode("utf8"), mimetype="application/json")
        except Exception as e:
            data = {
                "status":404,
                "error":e.args
            }
            return data
        
    @http.route('/iscapop/add_donation/', auth='public', type="json", methods=["POST"])
    def addDonations(self, itemid=None, **kw):
        try:
            response = http.request.httprequest.json

            result = http.request.env["iscapop.donation_model"].sudo().create(response)
            data = {
                "status":201,
                "result": "Donation "+str(result.id)+" added succesfully!"
            }
            return data
        except Exception as e:
            data = {
                "status":404,
                "error":e
            }
            return data