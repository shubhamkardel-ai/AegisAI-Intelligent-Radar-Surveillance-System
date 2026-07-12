class SensorFusion:

    def __init__(self):
        self.matches = []

    def fuse(self, aircrafts, detections):

        self.matches.clear()

        for aircraft in aircrafts:

            best = None

            for detection in detections:

                name = detection["name"]

                if aircraft.type == "Enemy":

                    if name in ["person", "car", "truck", "bus"]:

                        best = detection
                        break

                elif aircraft.type == "Friendly":

                    if name == "person":
                        best = detection
                        break

            aircraft.camera_object = best

            self.matches.append(
                {
                    "aircraft": aircraft,
                    "camera": best
                }
            )

        return self.matches