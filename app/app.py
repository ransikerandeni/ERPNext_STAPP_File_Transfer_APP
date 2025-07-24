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
            process_excel(filepath, site_name)
            flash('Files copied successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Please upload an Excel (.xlsx) file.')
            return redirect(request.url)
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel(excel_path, site_name):
    df = pd.read_excel(excel_path)
    for _, row in df.iterrows():
        folder_name = str(row['Attached To Name'])
        file_url = str(row['File URL'])
        target_folder = os.path.join('output', folder_name)
        os.makedirs(target_folder, exist_ok=True)
        # Try both private and public paths
        private_path = os.path.join('sites', site_name, 'private', 'files', file_url)
        public_path = os.path.join('sites', site_name, 'public', 'files', file_url)
        if os.path.exists(private_path):
            shutil.copy(private_path, target_folder)
        elif os.path.exists(public_path):
            shutil.copy(public_path, target_folder)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
