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


def fetch_rto_data(plate):
    vehicles = [
        Vehicle("MH12AB1234", 160, 0.12, 30),
        Vehicle("DL9CG4545", 140, 0.09, 20),
        Vehicle("KA05AB6789", 120, 0.08, 18),
        Vehicle("AP02UV1234", 160, 0.13, 26),
        Vehicle("BR09WX5678", 130, 0.09, 18),
        Vehicle("CH18YZ9012", 170, 0.14, 31),
        Vehicle("HR05AA3456", 145, 0.10, 23),
        Vehicle("JK13BB7890", 180, 0.15, 36),
        Vehicle("AS21CC1234", 120, 0.08, 20),
        Vehicle("GA27DD5678", 155, 0.12, 27),
        Vehicle("TR30EE9012", 165, 0.13, 30),
        Vehicle("UK04FF3456", 135, 0.09, 19),
        Vehicle("HP19GG7890", 175, 0.14, 33),
        Vehicle("MH47HH1234", 140, 0.11, 25),
        Vehicle("DL8JJ5678", 185, 0.16, 38),
        Vehicle("KA51KK9012", 115, 0.07, 16),
        Vehicle("GJ32LL3456", 195, 0.17, 40),
        Vehicle("TN45MM7890", 125, 0.08, 17),
        Vehicle("UP58NN1234", 160, 0.12, 28),
        Vehicle("PB61PP5678", 150, 0.10, 22),
        Vehicle("RJ74QQ9012", 170, 0.13, 29),
        Vehicle("MP87RR3456", 130, 0.09, 21),
        Vehicle("KL92SS7890", 180, 0.15, 35),
        Vehicle("AP36TT1234", 155, 0.12, 26),
        Vehicle("BR42UU5678", 165, 0.13, 30),
        Vehicle("CH50VV9012", 135, 0.09, 18),
        Vehicle("HR68WW3456", 175, 0.14, 32),
        Vehicle("JK75XX7890", 145, 0.11, 24),
        Vehicle("AS83YY1234", 195, 0.17, 39),
        Vehicle("GA91ZZ5678", 120, 0.08, 20),
        Vehicle("TR02AA9012", 185, 0.16, 37),
        Vehicle("UK14BB3456", 140, 0.10, 23),
        Vehicle("HP28CC7890", 160, 0.12, 27),
        Vehicle("UK07AB1234", 155, 0.12, 28),
        Vehicle("UK01CD5678", 165, 0.13, 30),
        Vehicle("UK08EF9012", 135, 0.09, 22),
        Vehicle("UK04GH3456", 175, 0.14, 32),
        Vehicle("UK11IJ7890", 145, 0.11, 25),
        Vehicle("UK02KL1234", 185, 0.16, 35),
        Vehicle("UK09MN5678", 125, 0.08, 20),
        Vehicle("UK06OP9012", 160, 0.12, 27),
        Vehicle("UK12QR3456", 150, 0.10, 24),
        Vehicle("UK03ST7890", 170, 0.13, 29),
        Vehicle("UK10UV1234", 130, 0.09, 21),
        Vehicle("UK05WX5678", 195, 0.17, 38),
        Vehicle("UK07YZ9012", 140, 0.10, 23),
        Vehicle("UK08AA3456", 180, 0.15, 34),
        Vehicle("UK04BB7890", 115, 0.07, 16),
        Vehicle("UK11CC1234", 190, 0.16, 36),
        Vehicle("UK02DD5678", 155, 0.12, 26),
        Vehicle("UK09EE9012", 165, 0.13, 31),
        Vehicle("UK06FF3456", 135, 0.09, 19),
        Vehicle("UK12GG7890", 175, 0.14, 33),
        Vehicle("UK03HH1234", 120, 0.08, 18),
        Vehicle("UK10JJ5678", 185, 0.16, 37),
        Vehicle("UK05KK9012", 150, 0.11, 25),
        Vehicle("UK07LL3456", 160, 0.12, 28),
        Vehicle("UK08MM7890", 170, 0.13, 30),
        Vehicle("UK04NN1234", 145, 0.10, 24),
        Vehicle("UK11OO5678", 195, 0.17, 39),
        Vehicle("UK02PP9012", 125, 0.08, 20),
        Vehicle("UK09QQ3456", 180, 0.15, 34),
        Vehicle("UK06RR7890", 140, 0.10, 23),
        Vehicle("UK12SS1234", 155, 0.12, 27),
        Vehicle("UK03TT5678", 165, 0.13, 29),
        Vehicle("UK10UU9012", 135, 0.09, 22),
        Vehicle("UK05VV3456", 175, 0.14, 32),
        Vehicle("UK07WW7890", 130, 0.09, 21),
        Vehicle("UK08XX1234", 190, 0.16, 36),
        Vehicle("UK04YY5678", 150, 0.11, 26),
        Vehicle("UK11ZZ9012", 160, 0.12, 28),
        Vehicle("UK02AA3456", 170, 0.13, 30),
        Vehicle("UK09BB7890", 145, 0.10, 24),
        Vehicle("UK06CC1234", 185, 0.15, 35),
        Vehicle("UK12DD5678", 120, 0.08, 19),
        Vehicle("UK03EE9012", 195, 0.17, 38),
        Vehicle("UK10FF3456", 140, 0.10, 23),
        Vehicle("UK05GG7890", 155, 0.12, 27),
        Vehicle("UK07HH1234", 165, 0.13, 31),
        Vehicle("UK08II5678", 135, 0.09, 20),
        Vehicle("UK04JJ9012", 175, 0.14, 33),
        Vehicle("UK11KK3456", 125, 0.08, 18),
        Vehicle("UK02LL7890", 180, 0.15, 34),
    ]
    return get_pollution_data(plate, vehicles)


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
