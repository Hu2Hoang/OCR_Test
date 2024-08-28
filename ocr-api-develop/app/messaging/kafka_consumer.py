from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from app.schemas.sche_base import DataResponse
from fastapi.responses import JSONResponse
from app.helpers import kafka_helper
from app.common.config import settings
from pydantic import BaseModel
import logging, logging.config
import datetime
import json
import uuid

from app.services.detection_service.detect_text import TextDetectionService
from app.services.recognition_service.recognition_text import TextRecognitionService
from typing import List
from collections import defaultdict

class TestReq(BaseModel):
    key: str
    channelId: str
    message: str

class ImagePathRequest(BaseModel):
    image_path: str

async def consume_messages(db):
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_INTERNAL,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username=settings.KAFKA_USERNAME,
        sasl_plain_password=settings.KAFKA_PASSWORD
    )
    await consumer.start()

    try:
        async for msg in consumer:
            # Xử lý message tại đây
            message_value = msg.value.decode('utf-8')
            key = msg.key.decode('utf-8')
            print(key)
            print(f"Received message: {message_value}")
            
            await event_detect(message_value, db)
    finally:
        await consumer.stop()

async def consume_messages_recog(db):
    consumer = AIOKafkaConsumer(
        'text-detection',
        bootstrap_servers=settings.KAFKA_INTERNAL,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username=settings.KAFKA_USERNAME,
        sasl_plain_password=settings.KAFKA_PASSWORD
    )
    await consumer.start()

    try:
        async for msg in consumer:
            # Xử lý message tại đây
            key = msg.key.decode('utf-8')
            message_value = msg.value.decode('utf-8')
            print("1")
            await event_recognition(message_value, db)

    finally:
        await consumer.stop()

async def event_detect(event_data, db): 
    data = json.loads(event_data)
    image_path = data['payload']['IMAGE_PATH']

    predictions_by_page = await detect_text(image_path, db)
    data: TestReq = {
        "aggregate_type" : "DETECTION",
        "aggregate_id": data["aggregate_id"],
        "status": "PROCESSING",
        "payload": {
                "IMAGE_PATH": image_path,
                "DETECTION":predictions_by_page
                },
        "timestamp": str(datetime.datetime.now())
        }
    # print("data: ", data)
    header = {
        "event_type" : "CREATED",
        "id" : str(uuid.uuid4())
    }

    await kafka_helper.pushMessage( topic="text-detection",key=data["aggregate_id"],
                                        mess=data, header=header)
async def event_recognition(event_data, db):
    path = json.loads(event_data)
    image_path = path['payload']['IMAGE_PATH']
    detection = path['payload']['DETECTION']
    predictions_by_page = await recognition_text(image_path, detection)
    data: TestReq = {
        "aggregate_type" : "RECOGNITION",
        "aggregate_id": path['aggregate_id'],
        "status": "PROCESSING",
        "payload": {
                "IMAGE_PATH": image_path,
                "DETECTION":predictions_by_page
                },
        "type": "CCCD",
        "timestamp": str(datetime.datetime.now())
        
        }
    
    header = {
        "event_type" : "CREATED",
        "id" : str(uuid.uuid4())
    }

    await kafka_helper.pushMessage(topic="text-recognition", key=data["aggregate_id"], mess=data, header=header)

async def detect_text(image_path, db):
    service = TextDetectionService()
    images, names= service.load_image(image_path)
    det_predictions = service.detect_text(images)
    predictions_by_page = defaultdict(list)
    for idx, (pred, name, image) in enumerate(zip(det_predictions, names, images)):
        out_pred = pred.model_dump(exclude=["heatmap", "affinity_map"])
        out_pred["page"] = len(predictions_by_page[name]) + 1
        predictions_by_page[name].append(out_pred)

    return predictions_by_page[names[0]]


async def recognition_text(image_path, det_predictions):

    service_reg = TextRecognitionService()
    images, names= service_reg.load_image(image_path)
    
    predictions_by_image = service_reg.recognize_text(images, det_predictions)
    predictions_by_page = defaultdict(list)
    for idx, (pred, name, image) in enumerate(zip(predictions_by_image, names, images)):
        out_pred = pred.model_dump(exclude=["heatmap", "affinity_map"])
        out_pred["page"] = len(predictions_by_page[name]) + 1
        predictions_by_page[name].append(out_pred)
        
    return predictions_by_page
    