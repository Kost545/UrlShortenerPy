import hashlib
import base64

def get_short_url(longUrl, length=7):
    hash_bytes = hashlib.sha256(longUrl.encode('utf-8')).digest()
    b64 = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    return b64[:length]
