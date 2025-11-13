from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import tempfile
import shutil
import json
import platform
from pathlib import Path

# Get project root directory (parent of backend/python)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
BACKEND_CPP_DIR = os.path.join(PROJECT_ROOT, 'backend', 'cpp')

# Configure Flask with new paths
app = Flask(__name__, 
            template_folder=os.path.join(FRONTEND_DIR, 'templates'),
            static_folder=os.path.join(FRONTEND_DIR, 'static'))
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(DATA_DIR, 'processed')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'zip', 'bin'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def encrypt_files():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        action = request.form.get('action', 'encrypt').lower()
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Create a temporary directory for this operation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files to temp directory
            file_paths = []
            for file in files:
                if file and allowed_file(file.filename):
                    file_path = os.path.join(temp_dir, file.filename)
                    file.save(file_path)
                    file_paths.append(file.filename)
            
            if not file_paths:
                return jsonify({'error': 'No valid files uploaded'}), 400
            
            # Prepare the C++ executable path (handle Windows .exe extension)
            exe_ext = '.exe' if platform.system() == 'Windows' else ''
            cpp_executable = os.path.join(BACKEND_CPP_DIR, f'encrypt_decrypt{exe_ext}')
            if not os.path.exists(cpp_executable):
                return jsonify({'error': 'C++ executable not found. Please build the project first.'}), 500
            
            # Execute the C++ program
            try:
                process = subprocess.Popen(
                    [cpp_executable],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=BACKEND_CPP_DIR
                )
                
                # Send directory and action to the C++ program
                input_data = f"{temp_dir}\n{action}\n"
                stdout, stderr = process.communicate(input=input_data, timeout=300)
                
                if process.returncode != 0:
                    return jsonify({
                        'error': f'Encryption/Decryption failed: {stderr}',
                        'stdout': stdout
                    }), 500
                
                # Copy processed files to processed folder
                processed_files = []
                for root, dirs, files_in_dir in os.walk(temp_dir):
                    for file_name in files_in_dir:
                        src_path = os.path.join(root, file_name)
                        dst_path = os.path.join(PROCESSED_FOLDER, file_name)
                        shutil.copy2(src_path, dst_path)
                        processed_files.append(file_name)
                
                return jsonify({
                    'success': True,
                    'message': f'Successfully {action}ed {len(processed_files)} file(s)',
                    'files': processed_files,
                    'output': stdout
                })
                
            except subprocess.TimeoutExpired:
                process.kill()
                return jsonify({'error': 'Operation timed out'}), 500
            except Exception as e:
                return jsonify({'error': f'Execution error: {str(e)}'}), 500
                
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/process-directory', methods=['POST'])
def process_directory():
    try:
        data = request.json
        directory = data.get('directory', '').strip()
        action = data.get('action', 'encrypt').lower()
        
        if not directory:
            return jsonify({'error': 'Directory path not provided'}), 400
        
        if not os.path.exists(directory) or not os.path.isdir(directory):
            return jsonify({'error': 'Invalid directory path'}), 400
        
        # Prepare the C++ executable path (handle Windows .exe extension)
        exe_ext = '.exe' if platform.system() == 'Windows' else ''
        cpp_executable = os.path.join(BACKEND_CPP_DIR, f'encrypt_decrypt{exe_ext}')
        if not os.path.exists(cpp_executable):
            return jsonify({'error': 'C++ executable not found. Please build the project first.'}), 500
        
        # Execute the C++ program
        try:
            process = subprocess.Popen(
                [cpp_executable],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=BACKEND_CPP_DIR
            )
            
            # Send directory and action to the C++ program
            input_data = f"{directory}\n{action}\n"
            stdout, stderr = process.communicate(input=input_data, timeout=300)
            
            if process.returncode != 0:
                return jsonify({
                    'error': f'Encryption/Decryption failed: {stderr}',
                    'stdout': stdout
                }), 500
            
            # Count processed files
            file_count = sum([len(files) for r, d, files in os.walk(directory)])
            
            return jsonify({
                'success': True,
                'message': f'Successfully {action}ed files in directory',
                'file_count': file_count,
                'output': stdout
            })
            
        except subprocess.TimeoutExpired:
            process.kill()
            return jsonify({'error': 'Operation timed out'}), 500
        except Exception as e:
            return jsonify({'error': f'Execution error: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

