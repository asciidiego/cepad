import io

from PIL import Image
from redis import StrictRedis

REDIS_URL = "localhost"
REDIS_PORT = "6379"

redis_client = StrictRedis(REDIS_URL, port=REDIS_PORT)

def process_stream():
    sub = redis_client.pubsub()
    sub.subscribe("image_res")
    print("Subscribed to 'image_res' topic")

    i = 0
    for message in sub.listen():
        data = message["data"]

        if type(data) == int:
            continue

        image = Image.open(io.BytesIO(data))
        image.save(f"img_{i}.png")
        print(f"Saved image: img_{i}.png")
        i += 1

if __name__ == "__main__":
    process_stream()
