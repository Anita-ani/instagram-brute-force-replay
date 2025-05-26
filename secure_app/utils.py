import random
import time

def generate_code():
    return str(random.randint(100000, 999999))

def is_code_expired(timestamp):
    return (time.time() - timestamp) > 60  # 60 seconds
