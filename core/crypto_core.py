from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def _key(key: str) -> bytes:
    return key.encode().ljust(16, b"\0")[:16]

def aes_encrypt_text(text, key):
    cipher = AES.new(_key(key), AES.MODE_ECB)
    enc = cipher.encrypt(pad(text.encode(), 16))
    return base64.b64encode(enc).decode()

def aes_decrypt_text(text, key):
    cipher = AES.new(_key(key), AES.MODE_ECB)
    dec = cipher.decrypt(base64.b64decode(text))
    return unpad(dec, 16).decode(errors="ignore")
