#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เสิร์ฟ dashboard สำหรับพรีวิว (แก้ปัญหา os.getcwd ในบาง sandbox)"""
import http.server, socketserver, os, functools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 4173
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"serving {ROOT} at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
