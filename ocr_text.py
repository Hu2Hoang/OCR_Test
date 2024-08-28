import argparse
import json
import copy
from collections import defaultdict

from surya.input.langs import replace_lang_with_code, get_unique_langs
from surya.input.load import load_lang_file
from surya.model.detection.segformer import load_processor as load_detection_processor
from surya.model.recognition.model import load_model as load_recognition_model
from surya.model.recognition.processor import load_processor as load_recognition_processor
from surya.model.recognition.tokenizer import _tokenize
from surya.ocr import evaluate_ocr
from surya.postprocessing.text import draw_text_on_image_v2
from surya.settings import settings

from get_information import get_content, save_json, save_results
import os

# Text Recognition
def recognize_text(images, names, result_path, det_predictions, 
                   save_images=True,  lang_file=None, langs=None, type = 'pdf'):
    
    assert langs or lang_file, "Must provide either --langs or --lang_file"
    type = type.lower()
    
    if lang_file:
        langs = load_lang_file(lang_file, names)
        for lang in langs:
            replace_lang_with_code(lang)
        image_langs = langs
    else:
        langs = langs.split(",")
        replace_lang_with_code(langs)
        image_langs = [langs] * len(images)

    _, lang_tokens = _tokenize("", get_unique_langs(image_langs))
    rec_model = load_recognition_model(langs=lang_tokens)
    rec_processor = load_recognition_processor()
    
    predictions_by_image = evaluate_ocr(images, image_langs, det_predictions, rec_model, rec_processor)

    if save_images:
        for idx, (name, image, pred, langs) in enumerate(zip(names, images, predictions_by_image, image_langs)):

            bboxes = [l.bbox for l in pred.text_lines]
            pred_text = [l.text for l in pred.text_lines]
            pred_confidence = [l.confidence for l in pred.text_lines]

            page_image = draw_text_on_image_v2(bboxes, pred_text, pred_confidence, image.size, langs, has_math="_math" in langs)
            page_image.save(os.path.join(result_path, f"{name}_{idx}_text.png"))
    save_results(result_path, "results_reg.json", predictions_by_image, names, images)