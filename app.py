from flask import Flask, send_file

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def serve_index():
    return send_file('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json')

@app.route('/service-worker.js')
def serve_service_worker():
    return send_file('service-worker.js', mimetype='application/javascript')

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_file(f'images/{filename}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
