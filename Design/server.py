from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import cgi

class FileUploadHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
        )

        uploaded_file = form['file']
        
        if uploaded_file.file:
            # Save the uploaded file to the server
            with open(uploaded_file.filename, 'wb') as file:
                file.write(uploaded_file.file.read())

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'File "{uploaded_file.filename}" uploaded successfully\n'.encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Bad Request: File not provided\n')
    def do_GET(self):
        if self.path.startswith('/download'):
            self.handle_file_download()
        else:
            super().do_GET()

    def handle_file_download(self):
        file_path = os.path.join(directory, self.path[10:])  # Remove '/download/' from the path
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found: File not available for download\n')
# Specify the port on which you want to run the server
PORT = 80

# Change to the directory you want to serve files from
directory = ''

Handler = FileUploadHandler

with TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
