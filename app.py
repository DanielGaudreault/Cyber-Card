from flask import Flask, send_file, jsonify, render_template_string, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def serve_index():
    """Serve the main PWA business card"""
    try:
        return send_file('index.html')
    except Exception as e:
        return f"Error loading index.html: {str(e)}", 500

@app.route('/manifest.json')
def serve_manifest():
    """Serve the PWA manifest with correct headers"""
    response = send_file('manifest.json')
    response.headers['Content-Type'] = 'application/manifest+json'
    return response

@app.route('/service-worker.js')
def serve_service_worker():
    """Serve the service worker with correct headers"""
    response = send_file('service-worker.js')
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from images directory"""
    try:
        return send_from_directory('images', filename)
    except Exception as e:
        return f"Image not found: {filename}", 404

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        "status": "healthy",
        "app": "Capmatic Business Card PWA",
        "version": "3.0.0"
    })

@app.route('/offline')
def offline_page():
    """Offline fallback page"""
    offline_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Capmatic - Offline</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: #0a0a1a; 
                color: white; 
                text-align: center; 
                padding: 50px;
            }
            .container { 
                max-width: 400px; 
                margin: 0 auto; 
            }
            .icon { 
                font-size: 48px; 
                margin-bottom: 20px;
                color: #00f7ff;
            }
            button {
                background: #00f7ff;
                color: #0a0a1a;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">📱</div>
            <h1>You're Offline</h1>
            <p>Please check your internet connection and try again.</p>
            <p>Some features may not be available offline.</p>
            <button onclick="window.location.reload()">Retry</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(offline_html)

# Add CORS headers for PWA
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    print(f"🚀 Starting Capmatic PWA on port {port}")
    print(f"📱 Access at: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
