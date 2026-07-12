import math


class IntentAnalyzer:

    def __init__(self):
        pass

    def analyze(self, aircraft):

        speed = aircraft.speed

        vx = aircraft.vx
        vy = aircraft.vy

        heading = aircraft.heading

        center_x = 500
        center_y = 400

        dx = aircraft.x - center_x
        dy = aircraft.y - center_y

        distance = math.sqrt(dx * dx + dy * dy)

        # ---------------------------------------
        # Behaviour Rules
        # ---------------------------------------

        if speed < 1:
            return "Hovering"

        if distance < 120:

            if speed > 3:
                return "Possible Attack"

            return "Close Surveillance"

        if distance > 280:

            return "Border Patrol"

        if abs(vx) < 0.3 and abs(vy) < 0.3:

            return "Station Keeping"

        if heading > 250 and heading < 290:

            return "Retreating"

        if heading > 70 and heading < 110:

            return "Approaching"

        return "Normal Patrol"