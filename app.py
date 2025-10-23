from flask import Flask, send_file, jsonify, render_template_string
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
    """Serve the PWA manifest"""
    return send_file('manifest.json')

@app.route('/service-worker.js')
def serve_service_worker():
    """Serve the service worker"""
    return send_file('service-worker.js', mimetype='application/javascript')

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from images directory"""
    try:
        return send_file(f'images/{filename}')
    except Exception as e:
        return f"Image not found: {filename}", 404

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        "status": "healthy",
        "app": "Capmatic Business Card PWA",
        "version": "1.0.0"
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
