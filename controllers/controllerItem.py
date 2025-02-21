# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json

class controlerItem(http.Controller):
    @http.route(['/iscapop/get_items/','/iscapop/get_item/<int:itemid>'], auth='public', type="http")
    def getItems(self, itemid=None, **kw):
        try:
            if itemid == None:
                domain=[]
            else:
                domain=[("id","=",itemid)]

            items = http.request.env["iscapop.item_model"].sudo().search_read(domain,["name","description","condition","location_id","category_id","donation_id","donated","active"])
            data = {"status":200, "data": items}
            return http.Response(json.dumps(data).encode("utf8"), mimetype="application/json")
        except Exception as e:
            data = {
                "status":404,
                "error":e.args
            }
            return http.Response(json.dumps(data), mimetype="application/json")

    @http.route('/iscapop/add_item/', auth='public', type="json", methods=["POST"])
    def addItems(self, **kw):
        try:
            response = http.request.httprequest.json

            result = http.request.env["iscapop.item_model"].sudo().create(response)
            data = {
                "status":201,
                "result": "Item "+str(result.id)+" added succesfully!"
            }
            return data
        except Exception as e:
            data = {
                "status":404,
                "error":e
            }
            return data
        
    @http.route('/iscapop/mod_item/', auth='public', type="json", methods=["PUT"])
    def modItems(self, **kw):
        try:
            response = http.request.httprequest.json

            result = http.request.env["iscapop.item_model"].sudo().search([("id","=",response["id"])])
            result.sudo().write(response)
            data = {
                "status":201,
                "result": "Item "+str(response["id"])+" modified succesfully!"
            }
            return data
        except Exception as e:
            data = {
                "status":404,
                "error":e
            }
            return data
        
    @http.route('/iscapop/del_item', auth="public", type="json", methods=["DELETE"])
    def deleteItems(self, **kw):
        response = http.request.httprequest.json
        domain = [("id", "=", response["id"])]
        try:
            http.request.env["iscapop.item_model"].sudo().search(domain).unlink()
            data = {"status": 200, "result": "Item deleted"}
            return data
        except Exception as e:
            data = {"status": 404, "error": e}
            return data