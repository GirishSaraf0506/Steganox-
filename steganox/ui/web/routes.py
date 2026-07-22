"""Flask route definitions."""

import os

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from steganox.core.steganography import SteganoxEngine
from steganox.core.validation import validate_image

engine = SteganoxEngine()
ALLOWED_EXTENSIONS = {"png", "bmp", "jpg", "jpeg"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def register_routes(app: Flask):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/embed", methods=["POST"])
    def embed():
        image = request.files.get("image")
        message = request.form.get("message", "").strip()
        password = request.form.get("password", "")
        if not image or not message or not password:
            return jsonify({"error": "image, message, and password are required."}), 400
        if not _allowed(image.filename):
            return jsonify({"error": "Unsupported image format."}), 400

        filename = secure_filename(image.filename)
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], f"stego_{filename}")
        image.save(input_path)

        valid, msg = validate_image(input_path)
        if not valid:
            return jsonify({"error": msg}), 400

        try:
            result = engine.embed(input_path, message, password)
            result.save(output_path)
            return send_file(
                output_path, as_attachment=True, download_name=f"stego_{filename}"
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {e}"}), 500

    @app.route("/api/extract", methods=["POST"])
    def extract():
        image = request.files.get("image")
        password = request.form.get("password", "")
        if not image or not password:
            return jsonify({"error": "image and password are required."}), 400
        if not _allowed(image.filename):
            return jsonify({"error": "Unsupported image format."}), 400

        filename = secure_filename(image.filename)
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(input_path)

        try:
            message = engine.extract(input_path, password)
            return jsonify({"success": True, "message": message})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {e}"}), 500
