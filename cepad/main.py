import io
import os
import time

from redis import StrictRedis
from PIL import Image, ImageDraw

cuda_enabled = os.system("nvcc --version | grep -c nvcc | sed 's/1/Enabled/'")


REDIS_URL = os.getenv("REDIS_URL", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = StrictRedis(REDIS_URL, port=REDIS_PORT)

def generate_image(message):

    msg = str(message["data"])

    NUM_IMAGES = 10
    for i in range(NUM_IMAGES):
        print(f"Creating image {i} with label: {msg}")
        time.sleep(5)
        image = Image.new('RGB', (400, 400), color = 'pink')
        draw = ImageDraw.Draw(image)
        W, H = image.size
        w, h = draw.textsize(msg + str(i))

        draw.text(((W - w) / 4, (H - h) / 4), f"[CUDA:{cuda_enabled}"]: {msg}-{i}", (255, 255, 255))

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        
        print(f"Publishing image {i}")
        redis_client.publish("image_res", img_byte_arr.getvalue())


if __name__ == "__main__":
    pubsub = redis_client.pubsub()
    pubsub.subscribe("jobs")
    for message in pubsub.listen():
        if "type" in message and message["type"] == 'subscribe':
            print("Handshake received.")
            continue

        print(f"New message: {message}")
        new_job = redis_client.lpop("jobs")
        if new_job:
            generate_image(message)
