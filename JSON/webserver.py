from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import DB
import product

class WebRequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/vnd.api+json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/products':
            product = DB.get_all()            
            self._set_response(200)
            d = { "data" : []}
            for i, tup in enumerate(product):
                d["data"].append({"type": "products", "id": tup[0], "attributes": {"marca": tup[3], "nome": tup[1], "prezzo": tup[2]}})
                                 
            self.wfile.write(json.dumps(d).encode('utf-8'))

        elif self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
            product = DB.get_product_by_id(product_id)
            if product:
                self._set_response(200)
                data = {"data": {"type": "products", "id": product[0], "attributes": {"marca": product[2], "nome": product[1], "prezzo": product[3]}}}
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self._set_response(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            marca = data["data"]["attributes"]['marca']
            nome = data["data"]["attributes"]['nome']
            prezzo = data["data"]["attributes"]['prezzo']
            new_product = DB.insert(marca, nome, prezzo)
            self._set_response(201)
            response = {"data": {"type": "products", "id": new_product[0], "attributes": {"marca": new_product[2], "nome": new_product[1], "prezzo": new_product[3]}}}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))
            
    def do_PATCH(self):
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = json.loads(patch_data.decode('utf-8'))
            product = DB.update(product_id, data)
            response = {"data": {"type": "products", "id": product[0], "attributes": {"marca": product[2], "nome": product[1], "prezzo": product[3]}}}
            print(response)
            self._set_response(200)
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_DELETE(self):
        path = self.path
        print(path)
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]       
            product = DB.delete(product_id)
            if(product):
                self._set_response(204)
            else:
                self._set_response(404)
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))

if __name__ == "__main__":
    server_address = ('localhost', 8888)
    server = HTTPServer(server_address, WebRequestHandler)
    server.serve_forever()
