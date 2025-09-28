import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import base64
import os
from pathlib import Path

DATA_PATH = Path('dsa/transactions.json')
HOST = '0.0.0.0'
PORT = 8000

import os
...
VALID_USER = os.environ.get('MOMO_USER', 'student')
VALID_PASS = os.environ.get('MOMO_PASS', 'password123')


def check_auth_header(header_value):
    if not header_value:
        return False
    if not header_value.startswith('Basic '):
        return False
    encoded = header_value.split(' ', 1)[1]
    try:
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        return username == VALID_USER and password == VALID_PASS
    except Exception:
        return False

class SimpleRESTHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send_json(self, status, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def auth_required(self):
        auth = self.headers.get('Authorization')
        if not check_auth_header(auth):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="MoMoAPI"')
            self.end_headers()
            return True
        return False

    def do_GET(self):
        if self.auth_required():
            return
        parsed = urlparse(self.path)
        parts = parsed.path.strip('/').split('/')
        if len(parts) == 1 and parts[0] == 'transactions':
           
            self.send_json(200, list(DATA_LIST))
            return
        if len(parts) == 2 and parts[0] == 'transactions':
            try:
                tid = int(parts[1])
            except:
                self.send_json(400, {'error': 'invalid id'})
                return
            tx = DATA_DICT.get(tid)
            if not tx:
                self.send_json(404, {'error': 'not found'})
                return
            self.send_json(200, tx)
            return
        self.send_json(404, {'error': 'not found'})

    def do_POST(self):
        if self.auth_required():
            return
        if self.path.strip('/') != 'transactions':
            self.send_json(404, {'error': 'not found'})
            return
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8') if length else '{}'
        try:
            payload = json.loads(raw)
        except:
            self.send_json(400, {'error': 'invalid json'})
            return
        new_id = max(DATA_DICT.keys(), default=0) + 1
        payload['id'] = new_id
        DATA_LIST.append(payload)
        DATA_DICT[new_id] = payload
        persist()
        self.send_json(201, payload)

    def do_PUT(self):
        if self.auth_required():
            return
        parts = self.path.strip('/').split('/')
        if len(parts) != 2 or parts[0] != 'transactions':
            self.send_json(404, {'error': 'not found'})
            return
        try:
            tid = int(parts[1])
        except:
            self.send_json(400, {'error': 'invalid id'})
            return
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8') if length else '{}'
        try:
            payload = json.loads(raw)
        except:
            self.send_json(400, {'error': 'invalid json'})
            return
        if tid not in DATA_DICT:
            self.send_json(404, {'error': 'not found'})
            return
        payload['id'] = tid
       
        for i, item in enumerate(DATA_LIST):
            if item.get('id') == tid:
                DATA_LIST[i] = payload
                break
        DATA_DICT[tid] = payload
        persist()
        self.send_json(200, payload)

    def do_DELETE(self):
        if self.auth_required():
            return
        parts = self.path.strip('/').split('/')
        if len(parts) != 2 or parts[0] != 'transactions':
            self.send_json(404, {'error': 'not found'})
            return
        try:
            tid = int(parts[1])
        except:
            self.send_json(400, {'error': 'invalid id'})
            return
        if tid not in DATA_DICT:
            self.send_json(404, {'error': 'not found'})
            return
       
        DATA_DICT.pop(tid)
        for i, item in enumerate(DATA_LIST):
            if item.get('id') == tid:
                DATA_LIST.pop(i)
                break
        persist()
        self.send_json(200, {'deleted': tid})

def persist():
    with DATA_PATH.open('w', encoding='utf8') as f:
        json.dump(DATA_LIST, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    if not DATA_PATH.exists():
        print('Data file not found; run dsa/parse_xml.py first')
        exit(1)
    with DATA_PATH.open('r', encoding='utf8') as f:
        DATA_LIST = json.load(f)
    DATA_DICT = { int(item['id']): item for item in DATA_LIST if 'id' in item }
    server = HTTPServer((HOST, PORT), SimpleRESTHandler)
    print(f'Serving on http://{HOST}:{PORT}  (Basic Auth user={VALID_USER})')
    server.serve_forever()
