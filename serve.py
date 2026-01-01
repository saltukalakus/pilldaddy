#!/usr/bin/env python3
"""
Simple HTTP server for local development of PillDaddy website.
Usage: python serve.py [port]
Default port: 8000
"""

import http.server
import socketserver
import sys
import os

# Default port
PORT = 8000

# Get port from command line argument if provided
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port number: {sys.argv[1]}")
        print("Usage: python serve.py [port]")
        sys.exit(1)

# Change to the directory where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Custom handler to set correct MIME types
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add custom headers if needed
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Customize log format
        print(f"[{self.log_date_time_string()}] {format % args}")

# Create the server
Handler = CustomHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 PillDaddy local server running at:")
        print(f"   http://localhost:{PORT}")
        print(f"   http://127.0.0.1:{PORT}")
        print(f"\n📄 Available pages:")
        print(f"   - http://localhost:{PORT}/index.html")
        print(f"   - http://localhost:{PORT}/terms-of-service.html")
        print(f"   - http://localhost:{PORT}/privacy.html")
        print(f"\n💡 Press Ctrl+C to stop the server\n")
        
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n👋 Server stopped.")
    sys.exit(0)
except OSError as e:
    if e.errno == 48 or e.errno == 98:  # Address already in use
        print(f"❌ Error: Port {PORT} is already in use.")
        print(f"   Try a different port: python serve.py [port]")
        sys.exit(1)
    else:
        raise
