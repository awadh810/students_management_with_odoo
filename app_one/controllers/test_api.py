from odoo import http
from odoo.http import request

class TestApi(http.Controller):
   
    @http.route("/api/test", methods=["GET"], type="http", auth="none", csrf=False)
    def test(self):
        # طباعة للسجل للتأكد أن الدالة تُستدعى
        print('API Endpoint "/api/test" was called') 
        
    
