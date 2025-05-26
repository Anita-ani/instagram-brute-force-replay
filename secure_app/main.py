from fastapi import FastAPI, Request, Query, HTTPException
from database import users, reset_codes, failed_attempts
from utils import generate_code, is_code_expired
from logger import log_access
import time

app = FastAPI(title="Instagram Replay – Secure Version")

@app.post("/reset/send-code")
def send_code(email: str = Query(...)):
    if email not in users:
        log_access(email, "Blocked (user not found)", "secure")
        raise HTTPException(status_code=404, detail="User not found")

    code = generate_code()
    reset_codes[email] = {"code": code, "timestamp": time.time(), "used": False}
    failed_attempts[email] = 0
    log_access(email, f"Sent code {code}", "secure")
    return {"detail": "Verification code sent (simulated)"}


@app.post("/reset/verify-code")
def verify_code(request: Request, email: str = Query(...), code: str = Query(...)):
    ip = request.client.host
    record = reset_codes.get(email)

    if not record:
        log_access(f"{ip}|{email}", "Blocked (no code sent)", "secure")
        return {"detail": "No code has been sent for this email"}

    if record["used"]:
        log_access(f"{ip}|{email}", "Blocked (code already used)", "secure")
        return {"detail": "This code has already been used"}

    if is_code_expired(record["timestamp"]):
        log_access(f"{ip}|{email}", "Blocked (code expired)", "secure")
        return {"detail": "Code expired, please request a new one"}

    if failed_attempts.get(email, 0) >= 5:
        log_access(f"{ip}|{email}", "Blocked (too many attempts)", "secure")
        return {"detail": "Too many failed attempts. Try again later."}

    if code == record["code"]:
        record["used"] = True
        log_access(f"{ip}|{email}", "Allowed (code match)", "secure")
        return {"detail": "Code verified, proceed to reset password"}
    else:
        failed_attempts[email] += 1
        log_access(f"{ip}|{email}", f"Blocked (invalid code {code})", "secure")
        return {"detail": "Invalid code"}
