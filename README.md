# Instagram Brute-Force Replay

This project simulates a real-world API business logic flaw inspired by Instagram's password reset bypass vulnerability. It includes both an insecure and a secure version to demonstrate exploitation and remediation.

## 🔓 Insecure App

| Endpoint                       | Method | Description                            |
|--------------------------------|--------|----------------------------------------|
| `/reset/send-code`            | POST   | Sends 6-digit code (no auth, no limit) |
| `/reset/verify-code`          | POST   | Allows unlimited guessing              |

- No rate-limiting
- No code expiration
- Logs brute-force attempts

## 🛡️ Secure App

| Endpoint                       | Method | Description                              |
|--------------------------------|--------|------------------------------------------|
| `/reset/send-code`            | POST   | Sends code + starts 60s timer            |
| `/reset/verify-code`          | POST   | Validates code with lockout + expiry     |

Fixes:
- Limits to 5 attempts
- Code expires in 60s
- Code can only be used once

## 🚀 How to Run

### 1. Install requirements
```bash
pip install -r requirements.txt

2. Start insecure app
cd insecure_app
uvicorn main:app --reload --port 8020

3. Start secure app
cd ../secure_app
uvicorn main:app --reload --port 8021

4. Testing
# Send code
curl -X POST "http://127.0.0.1:8020/reset/send-code?email=anita@insta.com"

# Brute-force guess
curl -X POST "http://127.0.0.1:8020/reset/verify-code?email=anita@insta.com&code=111111"

Educational Use Only
This repo is for training and research purposes.
