from flask import Flask, request, render_template, redirect, url_for, flash
import os
import pandas as pd
import shutil
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    logs = []
    if request.method == 'POST':
        site_name = request.form.get('site_name', '').strip()
        if not site_name:
            flash('Site name is required.')
            return redirect(request.url)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logs = process_excel(filepath, site_name)
            if any("Copied from" in log for log in logs):
                flash('Files copied successfully!')
            else:
                flash('No files were copied. Check the logs for details.')
            return render_template('index.html', logs=logs)
        else:
            flash('Invalid file type. Please upload an Excel (.xlsx) file.')
            return redirect(request.url)
    return render_template('index.html', logs=logs)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel(excel_path, site_name):
    df = pd.read_excel(excel_path)
    missing_files = []
    logs = []
    # Use the known frappe-bench path
    frappe_bench_base = '/home/erpuser/frappe-bench'
    frappe_sites_base = os.path.join(frappe_bench_base, 'sites')
    for _, row in df.iterrows():
        folder_name = str(row['Attached To Name']).strip()
        file_url = str(row['File URL']).strip()
        # Clean up the file_url by removing any duplicate 'files/' in the path
        file_url = file_url.replace('files/files/', 'files/').lstrip('/')
        target_folder = os.path.join('/home/erpuser/frappe-bench/ERPNext_STAPP_File_Transfer_APP/output', folder_name)
        os.makedirs(target_folder, exist_ok=True)
        private_path = os.path.join(frappe_sites_base, site_name, 'private', file_url)
        public_path = os.path.join(frappe_sites_base, site_name, 'public', file_url)
        logs.append(f"Checking private path: {private_path}")
        logs.append(f"Checking public path: {public_path}")
        if os.path.exists(private_path):
            shutil.copy(private_path, target_folder)
            logs.append(f"Copied from private: {private_path} to {target_folder}")
        elif os.path.exists(public_path):
            shutil.copy(public_path, target_folder)
            logs.append(f"Copied from public: {public_path} to {target_folder}")
        else:
            missing_files.append(file_url)
            logs.append(f"Missing file: {file_url}")
    if missing_files:
        logs.append(f"Missing files: {missing_files}")
    return logs

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
