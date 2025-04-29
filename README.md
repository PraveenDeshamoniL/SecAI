# Unified Threat, Malware, and Phishing Scanner

## How to Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## How to Deploy on Render
- Push this repo to GitHub
- Create new Render Web Service
- Set:
  - Build Command: pip install -r requirements.txt
  - Start Command: python app.py
- Done!
