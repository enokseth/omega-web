import json
import csv
from io import BytesIO
from flask import send_file

def save_json_line_by_line(data, file_name):
    with open(file_name, 'a') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write("\n")

def read_file(file_path, file_format):
    if file_format == 'text':
        with open(file_path, 'r') as file:
            data = file.read()
            return parse_text_data(data)
    elif file_format == 'json':
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON file: {e}")
                return None
            return data
    else:
        print("Unsupported file format")
        return None

def parse_text_data(data):
    entries = data.strip().split('\n\n')
    result = []
    for entry in entries:
        entry_data = {}
        for line in entry.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                entry_data[key] = value
        result.append(entry_data)
    return result

def download_json(results):
    json_data = json.dumps(results, indent=4)
    return send_file(BytesIO(json_data.encode()), mimetype='application/json', as_attachment=True, download_name='results.json')

def download_text(results):
    text_data = json.dumps(results, indent=4)
    return send_file(BytesIO(text_data.encode()), mimetype='text/plain', as_attachment=True, download_name='results.txt')

def download_csv(results):
    si = BytesIO()
    cw = csv.writer(si)
    headers = results['success'][0].keys()
    cw.writerow(headers)
    for result in results['success']:
        cw.writerow(result.values())
    for result in results['error']:
        cw.writerow(result.values())
    return send_file(BytesIO(si.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='results.csv')

def download_html(results):
    html_data = "<table border='1'>"
    html_data += "<tr>"
    for key in results['success'][0].keys():
        html_data += f"<th>{key}</th>"
    html_data += "</tr>"
    for result in results['success']:
        html_data += "<tr>"
        for value in result.values():
            html_data += f"<td>{value}</td>"
        html_data += "</tr>"
    for result in results['error']:
        html_data += "<tr>"
        for value in result.values():
            html_data += f"<td>{value}</td>"
        html_data += "</tr>"
    html_data += "</table>"
    return send_file(BytesIO(html_data.encode()), mimetype='text/html', as_attachment=True, download_name='results.html')
