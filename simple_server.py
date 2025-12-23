import http.server
import socketserver
import os

PORT = 8000

# Simple URL routing
URL_MAP = {
    '/': 'templates/home/index.html',
    '/about/': 'templates/about/index.html',
    '/blog/': 'templates/blog/index.html',
    '/blog/micromance/': 'templates/blog/micromance.html',
    '/blog/ai-matchmaking/': 'templates/blog/ai_matchmaking.html',
    '/blog/digital-boundaries/': 'templates/blog/digital_boundaries.html',
    '/tools/data-library/': 'templates/tools/data_library.html',
    '/tools/privacy/': 'templates/tools/privacy.html',
    '/tools/terms/': 'templates/tools/terms.html',
    '/directory/': 'templates/directory/index.html',
}

class DatingHubHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Map URL to file
        if self.path in URL_MAP:
            file_path = URL_MAP[self.path]
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
        
        # Default to file serving
        return super().do_GET()

os.chdir('.')
with socketserver.TCPServer(("", PORT), DatingHubHandler) as httpd:
    print(f"Serving Dating Hub at http://localhost:{PORT}")
    print("Available pages:")
    for url in URL_MAP.keys():
        print(f"  {url}")
    print("\nPress Ctrl+C to stop")
    httpd.serve_forever()
