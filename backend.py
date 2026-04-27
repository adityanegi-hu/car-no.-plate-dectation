import cv2
import os
import socket
from flask import Flask, render_template, request, jsonify, Response
from car import fetch_rto_data, pollution_score, detect_plate_region

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)
stop_camera = False

def _open_camera():
    """Try common camera backends/indexes for Windows webcams."""
    attempts = [
        (0, cv2.CAP_DSHOW),
        (0, None),
        (1, cv2.CAP_DSHOW),
        (1, None),
    ]
    for index, backend in attempts:
        cap = cv2.VideoCapture(index, backend) if backend is not None else cv2.VideoCapture(index)
        if cap.isOpened():
            return cap
        cap.release()
    return None

@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({"ok": True})

def camera_frames():
    global stop_camera
    stop_camera = False
    cap = _open_camera()
    if cap is None:
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
    def _find_free_port(start_port=5000, max_tries=20):
        for port in range(start_port, start_port + max_tries):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if sock.connect_ex(("127.0.0.1", port)) != 0:
                    return port
        return start_port

    env_port = os.environ.get("PORT")
    selected_port = int(env_port) if env_port else _find_free_port(5000)
    print(f"Starting backend on port {selected_port}")
    try:
        from waitress import serve
        print("Using Waitress WSGI server")
        serve(app, host="0.0.0.0", port=selected_port)
    except ImportError:
        print("Waitress not installed; using Flask dev server")
        print("Install with: pip install waitress")
        app.run(debug=True, use_reloader=False, host="0.0.0.0", port=selected_port)
