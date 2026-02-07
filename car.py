"""
Core logic for vehicle plate detection and pollution data lookup
"""
import cv2


# Structure to store vehicle pollution data
class Vehicle:
    def __init__(self, number_plate, co2_emission, nox_emission, pm25_level):
        self.number_plate = number_plate
        self.co2_emission = co2_emission
        self.nox_emission = nox_emission
        self.pm25_level = pm25_level


def get_pollution_data(number_plate, vehicles):
    """Get pollution data for a vehicle by plate number"""
    for vehicle in vehicles:
        if vehicle.number_plate == number_plate:
            return vehicle
    return Vehicle("", 0, 0.0, 0.0)


def pollution_score(vehicle):
    """Calculate pollution classification based on emissions"""
    score = 0
    if vehicle.co2_emission > 150:
        score += 2
    if vehicle.nox_emission > 0.1:
        score += 3
    if vehicle.pm25_level > 25:
        score += 1

    if score >= 5:
        return "High Pollution Vehicle"
    elif score >= 3:
        return "Moderate Pollution Vehicle"
    else:
        return "Low Pollution Vehicle"


def fetch_rto_data(number_plate):
    """Mock function to simulate fetching pollution data from RTO"""
    vehicles = [
        Vehicle("MH12AB1234", 160, 0.12, 30),
        Vehicle("DL9CG4545", 140, 0.09, 20),
        Vehicle("KA05AB6789", 120, 0.08, 18),
    ]
    return get_pollution_data(number_plate, vehicles)


def detect_plate_region(frame):
    """Detect license plate region using OpenCV edge detection and contours"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screen_cnt = None

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
        if len(approx) == 4:
            screen_cnt = approx
            break

    if screen_cnt is None:
        return None

    frame_with_contour = cv2.drawContours(
        frame.copy(), [screen_cnt], -1, (0, 255, 0), 3
    )
    return frame_with_contour


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        frame_with_contour = detect_plate_region(frame)
        if frame_with_contour is not None:
            cv2.imshow("License Plate Detected", frame_with_contour)
        else:
            cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
