import cv2

# Structure to store vehicle pollution data
class Vehicle:
    def __init__(self, number_plate, co2_emission, nox_emission, pm25_level):
        self.number_plate = number_plate
        self.co2_emission = co2_emission
        self.nox_emission = nox_emission
        self.pm25_level = pm25_level

# Function to get pollution data based on number plate
def get_pollution_data(number_plate, vehicles):
    for vehicle in vehicles:
        if vehicle.number_plate == number_plate:
            return vehicle
    return Vehicle("", 0, 0.0, 0.0)

# Function to calculate pollution score
def pollution_score(vehicle):
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

# Mock function to simulate fetching pollution data from RTO
def fetch_rto_data(number_plate):
    vehicles = [
        Vehicle("MH12AB1234", 160, 0.12, 30),
        Vehicle("DL9CG4545", 140, 0.09, 20),
        Vehicle("KA05AB6789", 120, 0.08, 18)
    ]
    return get_pollution_data(number_plate, vehicles)

# Function to detect license plate region using OpenCV
def detect_plate_region(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        return None

    # Draw the contour (license plate region) on the frame
    frame_with_contour = cv2.drawContours(frame.copy(), [screenCnt], -1, (0, 255, 0), 3)
    return frame_with_contour

# Open the default camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break

    # Detect license plate region
    frame_with_contour = detect_plate_region(frame)
    if frame_with_contour is not None:
        cv2.imshow("License Plate Detected", frame_with_contour)
    else:
        cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
