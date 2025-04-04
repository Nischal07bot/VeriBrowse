from flask import Flask, render_template, request, jsonify
import asyncio
from services.browser_interact import BrowserAIAgent

app = Flask(__name__)

# Initialize the BrowserAIAgent once at startup for better performance
browser_agent = BrowserAIAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/interact', methods=['POST'])
async def interact():
    """Handle browser interaction API requests"""
    try:
        data = request.json
        
        query = data.get('query')
        if not query:
            return jsonify({"status": "error", "message": "No query provided"}), 400
        
        # Use the image path from request or default to the preset one
        image_path = data.get('image_path', 'services/image.png')
        
        # Process the query with our agent
        result = await browser_agent.process_query(query, image_path)
        
        return jsonify({
            "status": "success", 
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error processing request: {str(e)}"
        }), 500

@app.route('/api/extract', methods=['POST'])
def extract():
    """Handle data extraction API requests"""
    try:
        if request.method == 'POST':
            data = request.json
            # Process your data here
            return jsonify({"status": "success", "message": "Data received"})
        return jsonify({"status": "ready"})
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error processing extraction: {str(e)}"
        }), 500

# Create a simple template directory and index.html file if it doesn't exist
@app.before_first_request
def create_templates():
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>VeriBrowse</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .input-section {
            margin-bottom: 20px;
        }
        #output {
            border: 1px solid #ddd;
            padding: 15px;
            min-height: 200px;
        }
        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>VeriBrowse</h1>
    <div class="input-section">
        <h3>Enter your browser task:</h3>
        <input type="text" id="query" placeholder="e.g., Find the price of iPhone on Amazon" style="width: 70%;">
        <button onclick="sendQuery()">Process</button>
    </div>
    
    <div>
        <h3>Output:</h3>
        <div id="output"></div>
    </div>

    <script>
        async function sendQuery() {
            const query = document.getElementById('query').value;
            if (!query) {
                alert('Please enter a query');
                return;
            }
            
            document.getElementById('output').innerText = 'Processing...';
            
            try {
                const response = await fetch('/api/interact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query }),
                });
                
                const data = await response.json();
                document.getElementById('output').innerText = data.result || data.message;
            } catch (error) {
                document.getElementById('output').innerText = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
            ''')

if __name__ == '__main__':
    app.run(debug=True)