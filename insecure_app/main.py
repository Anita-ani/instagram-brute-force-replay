from fastapi import FastAPI, Query
from database import users, reset_codes
from utils import generate_code
from logger import log_access

app = FastAPI(title="Instagram Replay – Insecure Version")

@app.post("/reset/send-code")
def send_code(email: str = Query(...)):
    if email not in users:
        log_access(email, "Blocked (user not found)", "insecure")
        return {"detail": "User not found"}

    code = generate_code()
    reset_codes[email] = code
    log_access(email, f"Sent code {code}", "insecure")
    return {"detail": "Verification code sent (simulated)"}


@app.post("/reset/verify-code")
def verify_code(email: str = Query(...), code: str = Query(...)):
    real_code = reset_codes.get(email)
    if not real_code:
        log_access(email, f"Blocked (no code sent)", "insecure")
        return {"detail": "No code has been sent for this email"}

    if code == real_code:
        log_access(email, "Allowed (code match)", "insecure")
        return {"detail": "Code verified, proceed to reset password"}
    else:
        log_access(email, f"Blocked (invalid code {code})", "insecure")
        return {"detail": "Invalid code"}
