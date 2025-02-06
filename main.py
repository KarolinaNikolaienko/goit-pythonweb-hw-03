import json
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self.path = 'index.html'

            if self.path.startswith('/'):
                self.path = self.path[1:]

            if self.path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/html'

            with open(self.path, 'rb') as file:
                self.send_response(200)
                self.send_header("Content-type", f"{content_type}; charset=utf-8")
                self.end_headers()
                self.wfile.write(file.read())

        except FileNotFoundError:
            with open("error.html", 'rb') as file:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(file.read())

    def do_POST(self):
        try:
            if self.path == "/message":
                data = self.rfile.read(int(self.headers['Content-Length']))
                data_parse = urllib.parse.unquote_plus(data.decode())
                data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

                with open("storage/data.json", "r") as file:
                    try:
                        json_data = json.load(file)
                        print(json_data)
                    except json.JSONDecodeError:
                        json_data = {}
                        print("empty")
                json_data[datetime.now().__str__()] = data_dict
                with open("storage/data.json", "w") as file:
                    json.dump(json_data, file, indent=4)

                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        except FileNotFoundError:
            print("File storage/data.json not found")
            self.send_response(404)
            self.send_header('Location', '/')
            self.end_headers()

def start_server():
    server_address = ('localhost', 3000)
    server = HTTPServer(server_address, HTTPRequestHandler)
    print("Server at /localhost:3000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server closed")

def main():
    start_server()


if __name__ == "__main__":
    main()