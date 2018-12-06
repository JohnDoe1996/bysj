from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

address = ("0.0.0.0",8888)

if __name__ == '__main__':
    httpd = HTTPServer(address,SimpleHTTPRequestHandler)
    print(address," 服务器正在运行，按Ctrl+C结束")
    httpd.serve_forever()