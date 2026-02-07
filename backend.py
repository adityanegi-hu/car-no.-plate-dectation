"""
Vehicle License Plate Detection & Pollution Lookup - Flask Backend
Integrates OpenCV plate detection with pollution data API
"""
import base64
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify

# Import logic from car.py
from car import (
    Vehicle,
    get_pollution_data,
    pollution_score,
    fetch_rto_data,
    detect_plate_region,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "webp",
        "bmp",
    }


@app.route("/")
def index():
    """Serve the main frontend page"""
    return render_template("index.html")


@app.route("/api/detect-plate", methods=["POST"])
def api_detect_plate():
    """
    Accept image upload, detect license plate region, return annotated image as base64
    """
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Invalid file type. Use PNG, JPG, JPEG, WEBP, BMP"}), 400

        # Read image bytes
        file_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"success": False, "error": "Could not decode image"}), 400

        # Detect plate region
        result_frame = detect_plate_region(frame)

        if result_frame is None:
            # No plate found, return original image
            _, buffer = cv2.imencode(".jpg", frame)
        else:
            _, buffer = cv2.imencode(".jpg", result_frame)

        img_base64 = base64.b64encode(buffer).decode("utf-8")
        plate_detected = result_frame is not None

        return jsonify({
            "success": True,
            "plate_detected": plate_detected,
            "image": f"data:image/jpeg;base64,{img_base64}",
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/pollution/<plate_number>")
def api_pollution(plate_number):
    """
    Get pollution data for a vehicle by plate number
    """
    try:
        if not plate_number or len(plate_number.strip()) == 0:
            return jsonify({"success": False, "error": "Plate number is required"}), 400

        plate_number = plate_number.strip().upper()
        vehicle = fetch_rto_data(plate_number)

        if vehicle.number_plate == "":
            return jsonify({
                "success": False,
                "error": f"No data found for plate: {plate_number}",
            }), 404

        classification = pollution_score(vehicle)
        return jsonify({
            "success": True,
            "vehicle": {
                "number_plate": vehicle.number_plate,
                "co2_emission": vehicle.co2_emission,
                "nox_emission": vehicle.nox_emission,
                "pm25_level": vehicle.pm25_level,
                "classification": classification,
            },
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
