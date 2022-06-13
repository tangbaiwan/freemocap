import logging
from datetime import datetime

import cv2
import numpy as np
from fastapi import APIRouter, WebSocket

from src.cameras.capture.dataclasses.frame_payload import FramePayload

logger = logging.getLogger(__name__)

cam_ws_router = APIRouter()


async def websocket_send(web_socket: WebSocket, input_payload: FramePayload):
    if not input_payload.success:
        return
    success, frame = cv2.imencode(".png", input_payload.image)
    if not success:
        return
    await web_socket.send_bytes(frame.tobytes())


@cam_ws_router.websocket("/ws/hello_world")
async def preview_webcam(web_socket: WebSocket):
    await web_socket.accept()
    while True:
        last_read = datetime.now()
        byte_data = await web_socket.receive_bytes()
        time_since = datetime.now()
        print("Per Frame Time: ", time_since - last_read)
        buffer = np.frombuffer(byte_data, dtype='uint8').reshape((600, 800, 4))
        buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)

