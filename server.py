#!/usr/bin/python3

""" A rough and ready Python server capable of serving HTML,
    JSON and .py CGI scripts and applying the CORS headers.
    Not suitable for use in production!
"""

from http.server import HTTPServer, CGIHTTPRequestHandler
from contextlib import redirect_stdout
import os
import subprocess

# change these as required
PORT = 8000
HOST = 'localhost'
ROOT = '.'

class CORSHTTPRequestHandler(CGIHTTPRequestHandler):

    def _set_html_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_api_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        """Handle a GET request."""
        # check the file extension...
        filename, extension = os.path.splitext(self.path)
        # if .html, try to read file and set HTML headers
        if extension == '.html' or extension == '.htm':
            try:
                self._set_html_headers()
                with open(ROOT + self.path) as f:
                    read_data = f.read()
                self.wfile.write(str.encode(read_data))
            except IOError:
                self.wfile.write(b'Error 404: File not found')
        # if .json, try to read and set JSON API headers
        elif extension == '.json':
            try:
                self._set_api_headers()
                with open(ROOT + self.path) as f:
                    read_data = f.read()
                self.wfile.write(str.encode(read_data))
            except IOError:
                self.wfile.write(b'Error 404: File not found')
        # if .py, try to serve script and set API headers
        elif extension == '.py':
            self._set_api_headers()
            self.run_cgi()
        # else look for an index.html page in root directory
        else:
            try:
                self._set_html_headers()
                with open(ROOT + '/index.html') as f:
                    read_data = f.read()
                self.wfile.write(str.encode(read_data))
            except IOError:
                self.wfile.write(b'Error 404: File not found')
    
    def run_cgi(self):
        """Execute a CGI script as a subprocess."""
        cmd = ['python', ROOT+self.path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        self.wfile.write(result.stdout)

    cgi_directories = ['/cgi-bin', '/htbin']

def run():
    print("Starting simple CGI/CORS server...")
    httpd = HTTPServer((HOST, PORT), CORSHTTPRequestHandler)
    print("Serving on port {}".format(PORT))
    httpd.serve_forever()

if __name__ == "__main__":
    run()
