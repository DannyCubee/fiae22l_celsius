import random
import urllib.request
from datetime import datetime

for x in range(0, 100):
    celsius = random.randint(-50, 100)
    fahrenheit = random.randint(-50, 100)
    client = {1: "RPI-1", 2: "RPI-2"}
    now = datetime.now()
    request = urllib.request.Request(f"http://192.168.2.100:8000/api/v1/new-temperatures?temp_c={celsius}&temp_f={fahrenheit}&client={client[random.randint(1,2)]}", method="POST")

    with urllib.request.urlopen(request) as response:
        response_data = response.read().decode("utf-8")
        print(response_data)
