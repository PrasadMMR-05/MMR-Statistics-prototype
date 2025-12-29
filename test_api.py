import urllib.request
import json
import time

url = "http://127.0.0.1:8000/generate"
data = {"query": "trends in Tech", "k": 3}
headers = {'Content-Type': 'application/json'}

print(f"Testing {url} with {data}...")

for i in range(5):
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print("Response received:")
            print(result)
            break
    except Exception as e:
        print(f"Attempt {i+1} failed: {e}")
        time.sleep(2)
