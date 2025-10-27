# 安装依赖：pip install flask
import json
import os
from flask import Flask, jsonify, request

# load config
with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def hello_world():
    return jsonify({"code": 0,"msg": "api service running"})

# api: /api/v1/list/floder
@app.route('/api/v1/list/floder')
def list_floder():
    notes_dir = 'notes'
    if not os.path.exists(notes_dir):
        return jsonify({"error": "Notes directory not found"}), 404

    folders = []
    for filename in os.listdir(notes_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(notes_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    folders.append(data)
                except json.JSONDecodeError:
                    # Handle cases where the file is not valid JSON
                    pass
    return jsonify(folders)

# api: /api/v1/list/getNoteInfo
@app.route('/api/v1/list/getNoteInfo')
def get_note_info():
    folder_name = request.args.get('flodername')
    note_name = request.args.get('notename')

    if not folder_name or not note_name:
        return jsonify({"code":0,"msg": "Missing flodername or notename parameter"}), 400

    file_path = os.path.join('notes', folder_name, f'{note_name}.json')

    if not os.path.exists(file_path):
        return jsonify({"code":0,"msg": "Note not found"}), 404

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return jsonify(data)
        except json.JSONDecodeError:
            return jsonify({"code":0,"msg": "Invalid JSON format"}), 500

# api: /api/v1/getNoteContent
@app.route('/api/v1/getNoteContent')
def get_note_content():
    folder_name = request.args.get('flodername')
    note_name = request.args.get('notename')

    if not folder_name or not note_name:
        return jsonify({"error": "Missing flodername or notename parameter"}), 400

    json_file_path = os.path.join('notes', folder_name, f'{note_name}.json')

    if not os.path.exists(json_file_path):
        return jsonify({"error": "Note JSON file not found"}), 404

    with open(json_file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 500

    note_content_filename = data.get('noteName')
    if not note_content_filename:
        return jsonify({"error": "noteName not found in JSON data"}), 404

    content_file_path = os.path.join('notes', folder_name, note_content_filename)

    if not os.path.exists(content_file_path):
        return jsonify({"error": "Note content file not found"}), 404

    with open(content_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data['content'] = content
    return jsonify(data)

if __name__ == '__main__':
    # 从配置中获取主机和端口，并提供默认值
    host = config.get('url', '0.0.0.0')
    port = int(config.get('port', 6600))
    # 监听配置的主机和端口，允许外部访问
    app.run(host=host, port=port, debug=True)
    