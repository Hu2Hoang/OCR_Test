from app.services.recognition_service.surya.input.langs import replace_lang_with_code, get_unique_langs
from app.services.recognition_service.surya.model.recognition.model import load_model as load_recognition_model
from app.services.recognition_service.surya.model.recognition.processor import load_processor as load_recognition_processor
from app.services.recognition_service.surya.model.recognition.tokenizer import _tokenize
from app.services.recognition_service.surya.ocr import evaluate_ocr_v2
from app.services.detection_service.surya.input.load import load_from_folder, load_from_file
import os
import numpy as np
import cv2


class TextRecognitionService:

    def __init__(self):
        pass

    def load_image(self, input_path, max_pages = None):
        if os.path.isdir(input_path):
            images, names = load_from_folder(input_path, max_pages)
        else:
            images, names = load_from_file(input_path, max_pages)

        return images, names
    
    def recognize_text(self, images, det_predictions, langs='vi'):
        langs = langs.split(",")
        replace_lang_with_code(langs)
        image_langs = [langs] * len(images)
        _, lang_tokens = _tokenize("", get_unique_langs(image_langs))
        rec_model = load_recognition_model(langs=lang_tokens)
        rec_processor = load_recognition_processor()
        predictions_by_image = evaluate_ocr_v2(images, image_langs, det_predictions, rec_model, rec_processor)
        return predictions_by_image
