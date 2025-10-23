from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/manifest.json')
def manifest():
    return send_file('manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_file('service-worker.js')

@app.route('/images/<path:filename>')
def images(filename):
    return send_file(f'images/{filename}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
