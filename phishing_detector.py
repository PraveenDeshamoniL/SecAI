
def predict_url(url):
    suspicious_keywords = ['login', 'verify', 'secure', 'update', 'account']
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        return "Phishing"
    return "Safe"
