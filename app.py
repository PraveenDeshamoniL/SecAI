
from flask import Flask, render_template, request
import os
import pandas as pd
from phishing_detector import predict_url
from malware_detector import check_malware
from train_model import train_model_if_needed
from risk_assessment import assess_risk
import joblib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
model = train_model_if_needed('pretrained/risk_model.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    phishing_result = ""
    malware_results = []
    threat_results = []

    if request.method == 'POST':
        # Phishing URL Check
        url = request.form.get('url')
        if url:
            phishing_result = predict_url(url)

        # Malware files check
        files = request.files.getlist('malware_files')
        for file in files:
            if file and file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                malware_status = check_malware(filepath)
                malware_results.append(f"{file.filename}: {'Malware' if malware_status else 'Clean'}")
                os.remove(filepath)

        # Threat Detection
        threat_file = request.files.get('threat_file')
        if threat_file and threat_file.filename.endswith('.csv'):
            df = pd.read_csv(threat_file, chunksize=1000)
            for chunk in df:
                if 'Flow Duration' in chunk.columns:
                    features = chunk[['Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts', 'Pkt Len Mean']]
                    preds = model.predict(features)
                    for pred in preds:
                        risk = assess_risk(pred)
                        threat_results.append(f"Threat: {pred}, Risk Level: {risk}")

    return render_template('home.html',
        phishing_result=phishing_result,
        malware_results=malware_results,
        threat_results=threat_results
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
