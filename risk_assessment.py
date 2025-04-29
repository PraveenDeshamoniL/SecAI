
def assess_risk(label):
    mapping = {
        'DDoS': 'Critical',
        'Botnet': 'High',
        'BruteForce': 'High',
        'PortScan': 'Medium',
        'Normal': 'Low'
    }
    return mapping.get(label, 'Unknown')
