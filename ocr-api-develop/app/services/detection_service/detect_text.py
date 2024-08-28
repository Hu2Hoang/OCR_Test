from app.services.detection_service.surya.model.detection.segformer import load_model as load_detection_model, load_processor as load_detection_processor
from app.services.detection_service.surya.detection import batch_text_detection
from app.services.detection_service.surya.input.load import load_from_folder, load_from_file

import numpy as np
import cv2
import os

class TextDetectionService:
    def __init__(self):
        pass

    def load_image(self, input_path, max_pages = None):
        print(3)

        images, names = load_from_file(input_path, max_pages)

        return images, names

    def detect_text(self, image):
        
        det_processor = load_detection_processor()
        det_model = load_detection_model()
        det_predictions = batch_text_detection(image, det_model, det_processor)
        return det_predictions