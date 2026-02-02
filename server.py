import http.server
import socketserver
import json
import os

PORT = 8000
DATA_FILE = 'data.json'

class DataHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 如果请求读取数据
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(json.dumps({"small": [], "big": [], "fixed": 691}).encode())
            return
        # 否则默认处理静态文件(index.html)
        super().do_GET()

    def do_POST(self):
        # 如果请求保存数据
        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 写入文件
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                f.write(post_data.decode())

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return

print(f"启动成功！请在浏览器打开: http://localhost:{PORT}")
print("数据将自动保存到当前目录的 data.json")

# 允许地址重用，防止重启报错
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), DataHandler) as httpd:
    httpd.serve_forever()