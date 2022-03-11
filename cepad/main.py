import io
import os
import time

from redis import StrictRedis
from PIL import Image, ImageDraw


REDIS_URL = os.getenv("REDIS_URL", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = StrictRedis(REDIS_URL, port=REDIS_PORT)

def generate_image(message):
    if "type" in message and message["type"] == 'subscribe':
        print("Handshake received.")
        return

    msg = str(message["data"])

    NUM_IMAGES = 10
    for i in range(NUM_IMAGES):
        print(f"Creating image {i}")
        time.sleep(0.5)
        image = Image.new('RGB', (100, 100), color = 'pink')
        draw = ImageDraw.Draw(image)
        W, H = image.size
        w, h = draw.textsize(msg + str(i))

        draw.text(((W - w) / 2, (H - h) / 2), msg + str(i), (255, 255, 255))

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        
        print(f"Publishing image {i}")
        redis_client.publish("image_res", img_byte_arr.getvalue())


if __name__ == "__main__":
    pubsub = redis_client.pubsub()
    pubsub.subscribe("image")
    for message in pubsub.listen():
        print(f"new msg: {message}")
        generate_image(message)
