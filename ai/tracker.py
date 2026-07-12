"""
AegisAI
Multi Object Tracker
--------------------
Tracks detected aircraft between frames.
"""


class Tracker:

    def __init__(self):

        self.objects = {}

    def update(self, detections):

        """
        detections will come from detector.py

        Example:
        [
            (x, y, w, h),
            (x, y, w, h)
        ]
        """

        self.objects = {}

        for i, detection in enumerate(detections):

            self.objects[i] = detection

        return self.objects

    def count(self):

        return len(self.objects)

    def clear(self):

        self.objects.clear()