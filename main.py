from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/api/interact', methods=['POST'])
def interact():
    if request.method == 'POST':
        data = request.json
        # Process your data here
        return jsonify({"status": "success", "message": "Data received"})
    return jsonify({"status": "ready"})

@app.route('/api/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        data = request.json
        # Process your data here
        return jsonify({"status": "success", "message": "Data received"})
    return jsonify({"status": "ready"})

if __name__ == '__main__':
    app.run(debug=True)