# -*- coding: utf-8 -*-
import datetime
from odoo import http
from odoo.http import json


class Iscapop(http.Controller):
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
        
    @http.route('/iscapop/add_categories/', auth='public', type="json", methods=["POST"])
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

    @http.route('/iscapop/delete_category', auth="public", type="json", methods=["DELETE"])
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

    @http.route('/iscapop/add_items/', auth='public', type="json", methods=["POST"])
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
        
    @http.route('/iscapop/mod_items/', auth='public', type="json", methods=["PUT"])
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
        
    @http.route('/iscapop/delete_item', auth="public", type="json", methods=["DELETE"])
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
        
    @http.route('/iscapop/add_donations/', auth='public', type="json", methods=["POST"])
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