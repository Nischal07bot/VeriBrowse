from flask import Flask, render_template, request, jsonify
from services.browser_interact import BrowserAIAgent

app = Flask(__name__)

@app.route('/api/interact', methods=['POST'])
async def interact():
    data = request.json
    
    query = data.get('query')
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    respone = await BrowserAIAgent(query)
    
    # Process your query here
    return jsonify({"status": "success", "message": respone})

@app.route('/api/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        data = request.json
        # Process your data here
        return jsonify({"status": "success", "message": "Data received"})
    return jsonify({"status": "ready"})

if __name__ == '__main__':
    app.run(debug=True)