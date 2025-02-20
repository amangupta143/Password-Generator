from flask import Flask, render_template, jsonify, request
import string
import random
import re
from pathlib import Path
import json

app = Flask(__name__)

class PasswordChecker:
    @staticmethod
    def check_password_strength(password):
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 10
        else:
            feedback.append("Password should be at least 8 characters")
        
        # Character variety checks
        if re.search(r'[A-Z]', password): score += 15
        else: feedback.append("Add uppercase letters")
        if re.search(r'[a-z]', password): score += 15
        else: feedback.append("Add lowercase letters")
        if re.search(r'\d', password): score += 15
        else: feedback.append("Add numbers")
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 15
        else: feedback.append("Add symbols")
        
        # Complexity bonus
        unique_chars = len(set(password))
        score += min(15, unique_chars // 2)
        
        # Determine strength level
        if score >= 90: strength = "Very Strong"
        elif score >= 70: strength = "Strong"
        elif score >= 50: strength = "Moderate"
        elif score >= 25: strength = "Weak"
        else: strength = "Very Weak"
        
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    chars = ''
    if use_uppercase: chars += string.ascii_uppercase
    if use_lowercase: chars += string.ascii_lowercase
    if use_numbers: chars += string.digits
    if use_symbols: chars += string.punctuation
    
    if not chars:
        return None
        
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def index():
    # Load saved preferences if they exist
    prefs = {
        "length": 12,
        "uppercase": True,
        "lowercase": True,
        "numbers": True,
        "symbols": True
    }
    
    if Path('preferences.json').exists():
        try:
            saved_prefs = json.loads(Path('preferences.json').read_text())
            prefs.update(saved_prefs)
        except:
            pass
            
    return render_template('index.html', preferences=prefs)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    
    # Save preferences
    with open('preferences.json', 'w') as f:
        json.dump(data, f)
    
    password = generate_password(
        length=int(data.get('length', 12)),
        use_uppercase=data.get('uppercase', True),
        use_lowercase=data.get('lowercase', True),
        use_numbers=data.get('numbers', True),
        use_symbols=data.get('symbols', True)
    )
    
    if not password:
        return jsonify({
            "error": "Please select at least one character type"
        }), 400
    
    strength_info = PasswordChecker.check_password_strength(password)
    
    return jsonify({
        "password": password,
        "strength": strength_info
    })

@app.route('/check', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')
    
    strength_info = PasswordChecker.check_password_strength(password)
    return jsonify(strength_info)

if __name__ == '__main__':
    app.run(debug=True)