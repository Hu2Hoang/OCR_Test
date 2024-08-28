import argparse
import json
import copy
from collections import defaultdict

from surya.input.load import load_from_folder, load_from_file
from surya.model.detection.segformer import load_model as load_detection_model, load_processor as load_detection_processor
from surya.ocr import adjust_y_coordinates
from surya.detection import batch_text_detection
from surya.postprocessing.affinity import draw_lines_on_image
from surya.postprocessing.heatmap import draw_polys_on_image
from surya.settings import settings

# from VietnameseOcrCorrection.inferenceModel import check_correct_ocr, count_words, check_correct_paragraph
from get_information import save_results
import os

# INPUT_PATH: the input path of the image
INPUT_PATH = 'image_test/textbook_text.jpg'

# TYPE: types of images to be processed. Ex: passport, cccd, pdf, ...
TYPE = "pdf"

# LANG: Specified language used. Ex: English: en, Vietnamese: vi
LANG = 'vi'

# Text Detection
def detect_bboxes(input_path, results_dir=os.path.join(settings.RESULT_DIR, "surya"), 
                  save_images=True, max_pages=None, start_page=0, type = 'pdf'):

    if os.path.isdir(input_path):
        images, names = load_from_folder(input_path, max_pages, start_page)
        folder_name = os.path.basename(input_path)
    else:
        images, names = load_from_file(input_path, max_pages, start_page, type)
        folder_name = os.path.basename(input_path).split(".")[0]

    result_path = os.path.join(results_dir, folder_name)

    os.makedirs(result_path, exist_ok=True)

    det_processor = load_detection_processor()
    det_model = load_detection_model()
    det_predictions = batch_text_detection(images, det_model, det_processor)

    if save_images:
        for idx, (image, pred, name) in enumerate(zip(images, det_predictions, names)):
            polygons = [p.polygon for p in pred.bboxes]

            polygons = [adjust_y_coordinates(polygon, 0, 0) for polygon in polygons] 
            confidences = [c.confidence for c in pred.bboxes]

            bbox_image = draw_polys_on_image(polygons, copy.deepcopy(image), confidences)
            bbox_image.save(os.path.join(result_path, f"{name}_{idx}_bbox.png"))

            column_image = draw_lines_on_image(pred.vertical_lines, copy.deepcopy(image))
            column_image.save(os.path.join(result_path, f"{name}_{idx}_column.png"))

    save_results(result_path, "results_det.json", det_predictions, names, images)

    return images, names, result_path, det_predictions