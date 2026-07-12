"""
AegisAI
Computer Vision Detection Module
--------------------------------
This module will detect aircraft, drones,
vehicles and other objects using YOLO.

Version : 1.0
"""


class Detector:

    def __init__(self):

        self.model = None
        self.model_name = "Not Loaded"

    def load_model(self):

        print("Loading AI Model...")

    def detect(self, frame):

        return []

    def get_model_name(self):

        return self.model_name