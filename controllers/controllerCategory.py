# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json

class controlerCategory(http.Controller):
    @http.route(['/iscapop/get_categories/','/iscapop/get_category/<int:catid>'], auth='public', type="http")
    def getCategories(self, catid=None, **kw):
        try:
            if catid == None:
                domain=[]
            else:
                domain=[("id","=",catid)]

            categories = http.request.env["iscapop.category_model"].sudo().search_read(domain,["name","description","fullName","item_ids","catParent_id","catChildren_ids"])
            data = {"status":200, "data": categories}
            return http.Response(json.dumps(data).encode("utf8"), mimetype="application/json")
        except Exception as e:
            data = {
                "status":404,
                "error":e.args
            }
            return data
        
    @http.route('/iscapop/add_category/', auth='public', type="json", methods=["POST"])
    def addCategories(self, **kw):
        try:
            response = http.request.httprequest.json

            result = http.request.env["iscapop.category_model"].sudo().create(response)
            data = {
                "status":201,
                "result": "Category "+str(result.id)+" added succesfully!"
            }
            return data
        except Exception as e:
            data = {
                "status":404,
                "error":e
            }
            return data
        
    @http.route('/iscapop/mod_category/', auth='public', type="json", methods=["PUT"])
    def modCategory(self, **kw):
        try:
            response = http.request.httprequest.json

            result = http.request.env["iscapop.category_model"].sudo().search([("id","=",response["id"])])
            result.sudo().write(response)
            data = {
                "status":201,
                "result": "Category "+str(response["id"])+" modified succesfully!"
            }
            return data
        except Exception as e:
            data = {
                "status":404,
                "error":e
            }
            return data

    @http.route('/iscapop/del_category', auth="public", type="json", methods=["DELETE"])
    def deleteCategories(self, **kw):
        response = http.request.httprequest.json
        domain = [("id", "=", response["id"])]
        try:
            http.request.env["iscapop.category_model"].sudo().search(domain).unlink()
            data = {"status": 200, "result": "Category deleted"}
            return data
        except Exception as e:
            data = {"status": 404, "error": e}
            return data