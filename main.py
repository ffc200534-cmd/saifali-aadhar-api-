from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# ---------- Auto-Detect Current Date (DD/MM/YYYY) ----------
CURRENT_DATE = datetime.now().strftime("%d/%m/%Y")

KEY_STORE = {
    "mysecretkey123": {
        "owner": "SAIF ALI🔥🔥🔥",
        "created_on": CURRENT_DATE,   # ✅ अब "issued_on" की जगह "created_on"
        "valid_days": 30
    }
}

# ---------- Aadhaar Data ----------
def fetch_data_by_aadhar(aadhar):
    return [
        {
            "aadhar": aadhar,
            "address": " Vill Mahuajhor!Kastha!P s Paraiya Kastha!Gaya!Bihar!824209 ",
            "alt": None,
            "circle": "AIRTEL BHR&JHR",
            "email": None,
            "fname": " Dharmendra Yadav ",
            "name": " Saroj Devi ",
            "num": "9661756498"
        }
    ]

# ---------- Key Validate (30 Days Expiry) ----------
def validate_key(api_key):
    key_info = KEY_STORE.get(api_key)
    if not key_info:
        return None, "Invalid API key", None
    
    # "created_on" को DD/MM/YYYY से Parse करें
    created_date = datetime.strptime(key_info["created_on"], "%d/%m/%Y")
    expiry_date = created_date + timedelta(days=key_info["valid_days"])
    
    if datetime.now() > expiry_date:
        return None, f"API key expired after {key_info['valid_days']} days.", None
    
    expiry_str = f"{expiry_date.day}/{expiry_date.month:02d}/{expiry_date.year}"
    return key_info, None, expiry_str

# ---------- Aadhaar Endpoint ----------
@app.route('/search/aadhar', methods=['GET'])
def search_aadhar():
    aadhar = request.args.get('aadhar')
    api_key = request.args.get('key')

    if not aadhar or not api_key:
        return jsonify({"error": "Missing 'aadhar' or 'key'"}), 400

    key_info, error, expiry_str = validate_key(api_key)
    if error:
        return jsonify({"error": error}), 401

    data = fetch_data_by_aadhar(aadhar)

    response = {
        "result": data,
        "status": "success",
        "powered_by": "@saifali883883",
        "api_info": {
            "key_owner": key_info["owner"],
            "valid_for_days": key_info["valid_days"],
            "created_on": key_info["created_on"],   # ✅ "issued_on" की जगह "created_on"
            "expiry": expiry_str
        }
    }
    return jsonify(response)

# ---------- Server Start ----------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
