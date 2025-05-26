users = {
    "anita@insta.com": {"id": 1, "username": "anita"},
    "john@insta.com": {"id": 2, "username": "john"},
}

reset_codes = {}  # email → { code, timestamp, used }
failed_attempts = {}  # email → attempt count
