import webview
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from base64 import urlsafe_b64decode
from json import loads, dumps


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        dat = loads(urlsafe_b64decode(self.path.strip("/")).decode("utf-8"))
        window.evaluate_js("create_message("+dumps(dat['uname'])+", "+dumps(dat['content'])+")")


server = HTTPServer(('', 5080), MyHandler)
Thread(target=server.serve_forever, daemon=True).start()

class Api:
    def __init__(self):
        pass

    def closebutton(self):
        window.destroy()

    def minbutton(self):
        window.minimize()


api = Api()
window = webview.create_window('mini discord window', 'htdoc/main.html', transparent=True, js_api=api, frameless=True, easy_drag=False, on_top=True, height=200, width=300)
webview.start(debug=True)