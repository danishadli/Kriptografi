from flask import Flask, render_template, request, jsonify, send_file
from core.crypto_core import aes_encrypt_text, aes_decrypt_text
from core.image_crypto import encrypt_image, decrypt_image
from core.sbox_builder import build_sbox
from core.sbox_analysis import analyze_sbox, export_excel

import os

app = Flask(__name__)
UPLOAD_DIR = "uploads"
EXPORT_DIR = "exports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

# ===== TEXT AES =====
@app.route("/text/encrypt", methods=["POST"])
def text_encrypt():
    d = request.json
    return jsonify({"result": aes_encrypt_text(d["text"], d["key"])})

@app.route("/text/decrypt", methods=["POST"])
def text_decrypt():
    d = request.json
    return jsonify({"result": aes_decrypt_text(d["text"], d["key"])})

# ===== IMAGE AES =====
@app.route("/image/encrypt", methods=["POST"])
def image_encrypt():
    f = request.files["image"]
    key = request.form["key"]
    path = os.path.join(UPLOAD_DIR, "in.png")
    f.save(path)
    out = encrypt_image(path, key)
    return send_file(out, mimetype="image/png")

@app.route("/image/decrypt", methods=["POST"])
def image_decrypt():
    f = request.files["image"]
    key = request.form["key"]
    path = os.path.join(UPLOAD_DIR, "enc.png")
    f.save(path)
    out = decrypt_image(path, key)
    return send_file(out, mimetype="image/png")

# ===== SBOX =====
@app.route("/sbox/<preset>")
def sbox(preset):
    s = build_sbox(preset)
    return jsonify([s[i:i+16] for i in range(0,256,16)])

@app.route("/analysis/<preset>")
def analysis(preset):
    return jsonify(analyze_sbox(build_sbox(preset)))

@app.route("/export/<preset>")
def export(preset):
    path = os.path.join(EXPORT_DIR, f"{preset}_analysis.xlsx")
    export_excel(build_sbox(preset), path)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
