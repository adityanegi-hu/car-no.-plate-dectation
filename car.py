import os
import csv
import cv2


class Vehicle:
    def __init__(self, plate, co2, nox, pm25):
        self.number_plate = plate
        self.co2_emission = co2
        self.nox_emission = nox
        self.pm25_level = pm25


def get_pollution_data(plate, vehicles):
    for v in vehicles:
        if v.number_plate == plate:
            return v
    return Vehicle("", 0, 0.0, 0.0)


def pollution_score(v):
    score = 0
    if v.co2_emission > 150:
        score += 2
    if v.nox_emission > 0.1:
        score += 3
    if v.pm25_level > 25:
        score += 1
    if score >= 5:
        return "High Pollution Vehicle"
    if score >= 3:
        return "Moderate Pollution Vehicle"
    return "Low Pollution Vehicle"


def _load_vehicles_from_csv():
    """Read all vehicle records from vehicles.csv once at startup."""
    path = os.path.join(os.path.dirname(__file__), "vehicles.csv")
    records = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                records.append(
                    Vehicle(
                        row["plate"],
                        float(row["co2"]),
                        float(row["nox"]),
                        float(row["pm25"]),
                    )
                )
    except FileNotFoundError:
       
        pass
    return records


_VEHICLES = _load_vehicles_from_csv()


def fetch_rto_data(plate):
    return get_pollution_data(plate, _VEHICLES)


def detect_plate_region(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(gray, 30, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            return cv2.drawContours(frame.copy(), [approx], -1, (0, 255, 0), 3)
    return None


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        out = detect_plate_region(frame) or frame
        cv2.imshow("Plate", out)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


