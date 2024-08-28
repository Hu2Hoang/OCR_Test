from typing import List
from PIL import Image
from collections import Counter
from app.services.recognition_service.model_ocr.model_paddle import perform_ocr
from app.services.recognition_service.model_ocr.model_vietocr import perform_vietocr

from app.services.recognition_service.surya.detection import batch_text_detection
from app.services.recognition_service.surya.input.processing import slice_polys_from_image, slice_bboxes_from_image, convert_if_not_rgb, slice_polys_from_image_v2
from app.services.recognition_service.surya.postprocessing.text import sort_text_lines
from app.services.recognition_service.surya.recognition import batch_recognition
from app.services.recognition_service.surya.schema import TextLine, OCRResult


def run_recognition(images: List[Image.Image], langs: List[List[str]], rec_model, rec_processor, bboxes: List[List[List[int]]] = None, polygons: List[List[List[List[int]]]] = None, batch_size=None) -> List[OCRResult]:
    assert bboxes is not None or polygons is not None
    assert len(images) == len(langs), "You need to pass in one list of languages for each image"

    images = convert_if_not_rgb(images)

    slice_map = []
    all_slices = []
    all_langs = []
    for idx, (image, lang) in enumerate(zip(images, langs)):
        if polygons is not None:
            slices = slice_polys_from_image(image, polygons[idx])
        else:
            slices = slice_bboxes_from_image(image, bboxes[idx])
        slice_map.append(len(slices))
        all_slices.extend(slices)
        all_langs.extend([lang] * len(slices))

    rec_predictions, _ = batch_recognition(all_slices, all_langs, rec_model, rec_processor, batch_size=batch_size)

    predictions_by_image = []
    slice_start = 0
    for idx, (image, lang) in enumerate(zip(images, langs)):
        slice_end = slice_start + slice_map[idx]
        image_lines = rec_predictions[slice_start:slice_end]
        slice_start = slice_end

        text_lines = []
        for i in range(len(image_lines)):
            if polygons is not None:
                poly = polygons[idx][i]
            else:
                bbox = bboxes[idx][i]
                poly = [[bbox[0], bbox[1]], [bbox[2], bbox[1]], [bbox[2], bbox[3]], [bbox[0], bbox[3]]]

            text_lines.append(TextLine(
                text=image_lines[i],
                polygon=poly
            ))

        pred = OCRResult(
            text_lines=text_lines,
            languages=lang,
            image_bbox=[0, 0, image.size[0], image.size[1]]
        )
        predictions_by_image.append(pred)

    return predictions_by_image

def adjust_y_coordinates(polygon, decrease_percentage, increase_percentage):
    min_y = min(polygon, key=lambda point: point[1])[1]
    max_y = max(polygon, key=lambda point: point[1])[1]

    adjusted_polygon = []
    for x, y in polygon:
        if y == min_y:
            adjusted_y = int(y * (1 - decrease_percentage / 100))
        elif y == max_y:
            adjusted_y = int(y * (1 + increase_percentage / 100))
        else:
            adjusted_y = y
        adjusted_polygon.append([x, adjusted_y])
    
    return adjusted_polygon

def predict_by_image(images, langs, det_predictions, slice_map, rec_predictions, confidence_scores):
    predictions_by_image = []
    slice_start = 0
    for idx, (image, det_pred, lang) in enumerate(zip(images, det_predictions, langs)):
        slice_end = slice_start + slice_map[idx]
        image_lines = rec_predictions[slice_start:slice_end]
        line_confidences = confidence_scores[slice_start:slice_end]
        slice_start = slice_end

        assert len(image_lines) == len(det_pred['bboxes'])

        lines = []
        for text_line, confidence, bbox in zip(image_lines, line_confidences, det_pred['bboxes']):
            lines.append(TextLine(
                text=text_line,
                polygon=bbox['polygon'],
                bbox=bbox['bbox'],
                confidence=confidence
            ))

        lines = sort_text_lines(lines)

        predictions_by_image.append(OCRResult(
            text_lines=lines,
            languages=lang,
            image_bbox=det_pred['image_bbox']
        ))

    return predictions_by_image

def run_ocr(images: List[Image.Image], langs: List[List[str]], det_model, det_processor, rec_model, rec_processor, batch_size=None) -> List[OCRResult]:
    images = convert_if_not_rgb(images)
    det_predictions = batch_text_detection(images, det_model, det_processor)

    all_slices = []
    slice_map = []
    all_langs = []

    for idx, (det_pred, image, lang) in enumerate(zip(det_predictions, images, langs)):
        polygons = [p.polygon for p in det_pred.bboxes]

        polygons = [adjust_y_coordinates(polygon, 0.1, 0.2) for polygon in polygons] 

        slices = slice_polys_from_image(image, polygons)
        slice_map.append(len(slices))
        all_langs.extend([lang] * len(slices))
        all_slices.extend(slices)

    rec_predictions, confidence_scores = batch_recognition(all_slices, all_langs, rec_model, rec_processor, batch_size=batch_size)

    return predict_by_image(images, langs, det_predictions, slice_map, rec_predictions, confidence_scores)

def run_ocr_v2(images: List[Image.Image], langs: List[List[str]], det_predictions, rec_model, rec_processor, batch_size=None) -> List[OCRResult]:

    all_slices = []
    slice_map = []
    all_langs = []

    for idx, (det_pred, image, lang) in enumerate(zip(det_predictions, images, langs)):
        polygons = [p.polygon for p in det_pred.bboxes]

        polygons = [adjust_y_coordinates(polygon, 0, 0) for polygon in polygons] 

        slices, _ = slice_polys_from_image_v2(image, polygons)
        slice_map.append(len(slices))
        all_langs.extend([lang] * len(slices))
        all_slices.extend(slices)

    rec_predictions, confidence_scores = batch_recognition(all_slices, all_langs, rec_model, rec_processor, batch_size=batch_size)

    return predict_by_image(images, langs, det_predictions, slice_map, rec_predictions, confidence_scores)

def recognition_ocr(images, model_ocr):
    texts = []
    scores = []
    for image in images:
        text, conf_text = model_ocr(image)
        texts.append(text)
        scores.append(conf_text)
    
    return texts, scores

def analysis_model(texts_model_1, confidences_model_1, texts_model_2, confidences_model_2, texts_model_3, confidences_model_3):
    texts_all_models = [texts_model_1, texts_model_2, texts_model_3]
    confidences_all_models = [confidences_model_1, confidences_model_2, confidences_model_3]

    num_indices = len(texts_model_1)

    final_texts = []
    final_scores = []

    for i in range(num_indices):
        original_texts_at_index = [texts_all_models[j][i] for j in range(len(texts_all_models))]
        cleaned_texts_at_index = [text.replace(" ", "") for text in original_texts_at_index]
        confidences_at_index = [confidences_all_models[j][i] for j in range(len(confidences_all_models))]

        text_counts = Counter(cleaned_texts_at_index)
        
        most_common_texts = text_counts.most_common()
        
        if most_common_texts[0][1] >= 2:
            indices = [j for j, cleaned_text in enumerate(cleaned_texts_at_index) if cleaned_text == most_common_texts[0][0]]

            max_confidence_index = max(indices, key=lambda x: confidences_at_index[x])
            final_texts.append(original_texts_at_index[max_confidence_index])
            final_scores.append(confidences_at_index[max_confidence_index])
        else:
            max_confidence_index = confidences_at_index.index(max(confidences_at_index))
            final_texts.append(original_texts_at_index[max_confidence_index])
            final_scores.append(confidences_at_index[max_confidence_index])

    return final_texts, final_scores

def evaluate_ocr(images: List[Image.Image], langs: List[List[str]], names, det_predictions, rec_model, rec_processor, batch_size=None) -> List[OCRResult]:
    all_slices = []
    slice_map = []
    all_langs = []
    all_slices_crop = []

    for idx, (det_pred, image, lang) in enumerate(zip(det_predictions[names[0]], images, langs)):
        polygons = [p.polygon for p in det_pred.bboxes]

        polygons = [adjust_y_coordinates(polygon, 0, 0) for polygon in polygons] 

        slices, slices_crop = slice_polys_from_image_v2(image, polygons)
        slice_map.append(len(slices))
        all_langs.extend([lang] * len(slices))
        all_slices.extend(slices)
        all_slices_crop.extend(slices_crop)

    surya_ocr_text, surya_ocr_text_confidence = batch_recognition(all_slices, all_langs, rec_model, rec_processor, batch_size=batch_size)
    viet_ocr_text, viet_ocr_confidence = recognition_ocr(all_slices_crop, perform_vietocr)
    paddle_ocr_text, paddle_ocr_confidence = recognition_ocr(all_slices_crop, perform_ocr)
    
    texts, scores = analysis_model(surya_ocr_text, surya_ocr_text_confidence, viet_ocr_text, viet_ocr_confidence, paddle_ocr_text, paddle_ocr_confidence)
    return predict_by_image(images, langs, det_predictions, slice_map, texts, scores)

def evaluate_ocr_v2(images: List[Image.Image], langs: List[List[str]], det_predictions, rec_model, rec_processor, batch_size=None) -> List[OCRResult]:
    all_slices = []
    slice_map = []
    all_langs = []
    all_slices_crop = []

    for idx, (det_pred, image, lang) in enumerate(zip(det_predictions, images, langs)):
        polygons = [p['polygon'] for p in det_pred['bboxes']]

        polygons = [adjust_y_coordinates(polygon, 0, 0) for polygon in polygons] 

        slices, slices_crop = slice_polys_from_image_v2(image, polygons)
        slice_map.append(len(slices))
        all_langs.extend([lang] * len(slices))
        all_slices.extend(slices)
        all_slices_crop.extend(slices_crop)

    surya_ocr_text, surya_ocr_text_confidence = batch_recognition(all_slices, all_langs, rec_model, rec_processor, batch_size=batch_size)
    viet_ocr_text, viet_ocr_confidence = recognition_ocr(all_slices_crop, perform_vietocr)
    paddle_ocr_text, paddle_ocr_confidence = recognition_ocr(all_slices_crop, perform_ocr)
    
    texts, scores = analysis_model(surya_ocr_text, surya_ocr_text_confidence, viet_ocr_text, viet_ocr_confidence, paddle_ocr_text, paddle_ocr_confidence)
    return predict_by_image(images, langs, det_predictions, slice_map, texts, scores)

def run_ocr_v3(images: List[Image.Image], langs: List[List[str]], det_predictions, rec_model, rec_processor, batch_size=None) -> List[OCRResult]:

    all_slices = []
    slice_map = []
    all_langs = []

    for idx, (det_pred, image, lang) in enumerate(zip(det_predictions, images, langs)):
        polygons = [p.polygon for p in det_pred.bboxes]

        polygons = [adjust_y_coordinates(polygon, 0, 0) for polygon in polygons] 

        slices , slices_crop = slice_polys_from_image_v2(image, polygons)
        slice_map.append(len(slices))
        all_langs.extend([lang] * len(slices))
        all_slices.extend(slices_crop)

    rec_predictions, confidence_scores = recognition_ocr(all_slices, perform_ocr)

    return predict_by_image(images, langs, det_predictions, slice_map, rec_predictions, confidence_scores)
