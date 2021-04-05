from app import config
from hmac import compare_digest

def authed(f, password):
    def updated_f():
        if compare_digest(password)
        f()
    return 