import requests
import numpy as np
import argparse  

parser = argparse.ArgumentParser(description="Send numbers to BentoML model on AWS")
parser.add_argument("numbers", type=float, nargs='+', help="Numbers to input into the model")
parser.add_argument("--host", type=str, default="51.20.124.10", help="AWS EC2 host (default: 51.20.124.10)")
parser.add_argument("--port", type=int, default=3000, help="Port (default: 3000)")
args = parser.parse_args()

d = args.numbers
print(f'Which number is bigger, {d[0]} or {d[1]}?')

# Make request to AWS EC2 instance
url = f"http://{args.host}:{args.port}/predict"
payload = {"data": d}


response = requests.post(url, json=payload)
response.raise_for_status()
    
result = response.json()
print(result)
    
p = np.argmax(result)
print(f'{d[p]} is bigger ({(result[0][p]*100):.3f}% chance)')