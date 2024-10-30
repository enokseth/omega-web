from flask import Flask, render_template, request, jsonify, send_file
from checkers.pma_checker import check_pma_connections
from utils.file_utils.file_utils import read_file, save_json_line_by_line, download_csv, download_html, download_json, download_text, parse_text_data
from utils.output_formated.country_flags import get_flag
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Register get_flag as a filter
@app.template_filter('get_flag')
def get_flag_filter(country):
    return get_flag(country)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/checker')
def checker():
    return render_template('checker.html')

@app.route('/connector')
def connector():
    return render_template('connector.html')

@app.route('/geolocator')
def geolocator():
    return render_template('geolocator.html')

@app.route('/generator')
def generator():
    return render_template('generator.html')

@app.route('/pma_checker', methods=['GET', 'POST'])
def pma_checker():
    if request.method == 'POST':
        file = request.files['file']
        file_format = request.form['file_format']
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            entries = read_file(file_path, file_format)
            if not entries:
                return render_template('pma_checker.html', error="No entries found or file format is not supported.")

            success_results, error_results = check_pma_connections(entries)
            return render_template('pma_checker.html', success_results=success_results, error_results=error_results)
    else:
        success_results = []
        error_results = []
        if os.path.exists('success.json'):
            with open('success.json', 'r') as f:
                for line in f:
                    success_results.append(json.loads(line))
        if os.path.exists('errors.json'):
            with open('errors.json', 'r') as f:
                for line in f:
                    error_results.append(json.loads(line))
        return render_template('pma_checker.html', success_results=success_results, error_results=error_results)

@app.route('/download/<format>', methods=['GET'])
def download_results(format):
    results = get_combined_results()
    if format == 'json':
        return download_json(results)
    elif format == 'text':
        return download_text(results)
    elif format == 'csv':
        return download_csv(results)
    elif format == 'html':
        return download_html(results)
    else:
        return "Invalid format"

def get_combined_results():
    success_results = []
    with open('success.json', 'r') as f:
        for line in f:
            success_results.append(json.loads(line))
    error_results = []
    with open('errors.json', 'r') as f:
        for line in f:
            error_results.append(json.loads(line))
    return {'success': success_results, 'error': error_results}

if __name__ == '__main__':
    app.run(debug=True)
