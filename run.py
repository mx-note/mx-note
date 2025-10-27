# 安装依赖：pip install flask
import json
import os
import time
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

# api: /api/v1/list/note
@app.route('/api/v1/list/note')
def list_note():
    folder_name = request.args.get('flodername')
    if not folder_name:
        return jsonify({"error": "Missing flodername parameter"}), 400

    folder_path = os.path.join('notes', folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    notes = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    notes.append(data)
                except json.JSONDecodeError:
                    pass
    return jsonify(notes)


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


## 写
### 创建文件夹/分类
# api: /api/v1/mkdir
@app.route('/api/v1/mkdir', methods=['GET'])
def mkdir():
    noteName = request.args.get('noteName')
    if not noteName:
        return jsonify({"code": 0, "msg": "noteName is required"}), 400

    father_floder = request.args.get('father-floder', 'default')

    note_dir = os.path.join('notes', father_floder)
    json_file_path = os.path.join(note_dir, f'{noteName}.json')

    if os.path.exists(json_file_path):
        return jsonify({"code": 0, "msg": "Note already exists"}), 400

    author = request.args.get('author', 'admin')
    description = request.args.get('description', '')
    level = request.args.get('level', 0)
    type = request.args.get('type', 'markdown')

    if not os.path.exists(note_dir):
        os.makedirs(note_dir)

    note_data = {
        "noteName": noteName,
        "father-floder": father_floder,
        "createTime": str(int(time.time())),
        "author": author,
        "description": description,
        "level": level,
        "type": type
    }

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(note_data, f, ensure_ascii=False, indent=4)

    if type == 'markdown':
        md_file_path = os.path.join(note_dir, f'{noteName}.md')
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(f'# {noteName}\n')

    return jsonify({"code": 1, "msg": "Note created successfully"}), 201


if __name__ == '__main__':
    # 从配置中获取主机和端口，并提供默认值
    host = config.get('url', '0.0.0.0')
    port = int(config.get('port', 6600))
    # 监听配置的主机和端口，允许外部访问
    app.run(host=host, port=port, debug=True)
    