from flask import Flask, send_file, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    try:
        return send_file('index.html')
    except Exception as e:
        return f"Error loading index.html: {str(e)}", 500

@app.route('/manifest.json')
def serve_manifest():
    try:
        return send_file('manifest.json')
    except Exception as e:
        return f"Error loading manifest: {str(e)}", 500

@app.route('/service-worker.js')
def serve_service_worker():
    try:
        return send_file('service-worker.js', mimetype='application/javascript')
    except Exception as e:
        return f"Error loading service worker: {str(e)}", 500

@app.route('/images/<path:filename>')
def serve_images(filename):
    try:
        return send_from_directory('images', filename)
    except Exception as e:
        return f"Image not found: {filename}", 404

# Serve any other static files
@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_file(filename)
    except:
        return "File not found", 404

if __name__ == '__main__':
    print("🚀 Starting Capmatic Business Card PWA...")
    print("📱 Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
