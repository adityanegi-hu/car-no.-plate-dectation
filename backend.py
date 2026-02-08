import cv2
from flask import Flask, render_template, request, jsonify, Response

from car import fetch_rto_data, pollution_score, detect_plate_region

app = Flask(__name__)
stop_camera = False


@app.route("/")
def home():
    return render_template("index.html")


def camera_frames():
    global stop_camera
    stop_camera = False
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return
    try:
        while not stop_camera:
            ok, frame = cap.read()
            if not ok:
                break
            out = detect_plate_region(frame)
            if out is None:
                out = frame
            _, jpg = cv2.imencode(".jpg", out)
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n"
    finally:
        cap.release()


@app.route("/video_feed")
def video_feed():
    return Response(camera_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/api/camera/stop", methods=["POST"])
def camera_stop():
    global stop_camera
    stop_camera = True
    return jsonify({"ok": True})


@app.route("/api/pollution/<plate>")
def pollution(plate):
    plate = (plate or "").strip().upper()
    if not plate:
        return jsonify({"ok": False, "error": "Enter plate number"}), 400
    v = fetch_rto_data(plate)
    if v.number_plate == "":
        return jsonify({"ok": False, "error": "No data for " + plate}), 404
    level = pollution_score(v)
    return jsonify({
        "ok": True,
        "vehicle": {
            "number_plate": v.number_plate,
            "co2_emission": v.co2_emission,
            "nox_emission": v.nox_emission,
            "pm25_level": v.pm25_level,
            "classification": level,
        },
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
