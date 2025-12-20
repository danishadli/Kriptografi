from PIL import Image
import numpy as np
from Crypto.Cipher import AES

def _key(key):
    return key.encode().ljust(16, b"\0")[:16]

def _process(path, key, mode):
    img = Image.open(path).convert("RGB")
    arr = np.array(img).flatten()
    cipher = AES.new(_key(key), AES.MODE_ECB)

    out = []
    for i in range(0, len(arr), 16):
        blk = bytes(arr[i:i+16].tolist()).ljust(16, b"\0")
        res = cipher.encrypt(blk) if mode=="enc" else cipher.decrypt(blk)
        out.extend(res)

    out = np.array(out[:len(arr)], dtype=np.uint8)
    out = out.reshape(img.size[1], img.size[0], 3)
    out_img = Image.fromarray(out)
    out_path = "uploads/enc.png" if mode=="enc" else "uploads/dec.png"
    out_img.save(out_path)
    return out_path

def encrypt_image(path, key):
    return _process(path, key, "enc")

def decrypt_image(path, key):
    return _process(path, key, "dec")
