from flask import Flask, render_template, request, jsonify, send_file
from core.crypto_core import aes_encrypt_text, aes_decrypt_text
from core.image_crypto import encrypt_image, decrypt_image
from core.sbox_builder import build_sbox
from core.sbox_analysis import analyze_sbox, export_excel

import os, uuid

app = Flask(__name__)
UPLOAD_DIR = "uploads"
EXPORT_DIR = "exports"

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/text/encrypt", methods=["POST"])
def text_encrypt():
    d = request.get_json()
    return jsonify({"result": aes_encrypt_text(d["text"], d["key"])})

@app.route("/text/decrypt", methods=["POST"])
def text_decrypt():
    d = request.get_json()
    return jsonify({"result": aes_decrypt_text(d["text"], d["key"])})

@app.route("/image/encrypt", methods=["POST"])
def image_encrypt():
    f = request.files["image"]
    key = request.form["key"]
    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(UPLOAD_DIR, filename)
    f.save(path)
    out = encrypt_image(path, key)
    return send_file(out, mimetype="image/png")

@app.route("/image/decrypt", methods=["POST"])
def image_decrypt():
    f = request.files["image"]
    key = request.form["key"]
    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(UPLOAD_DIR, filename)
    f.save(path)
    out = decrypt_image(path, key)
    return send_file(out, mimetype="image/png")

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
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)