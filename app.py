from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from utils.parser import parse_whatsapp_chat
from utils.extractor import extract_todos
from datetime import datetime


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_todos_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.txt'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        try:
            messages = parse_whatsapp_chat(filepath)
            todos = extract_todos(messages)
            
            # Add IDs to todos for tracking completion
            for i, todo in enumerate(todos):
                todo['id'] = f"todo_{i}_{hash(todo['task'])}"
            
            output_path = os.path.join('static', 'todos.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(todos, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                'success': True,
                'todos': todos,
                'download_url': '/download'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type. Please upload a .txt file'}), 400

@app.route('/download')
def download():
    return send_file('static/todos.json', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)