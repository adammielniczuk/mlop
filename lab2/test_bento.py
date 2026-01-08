import bentoml
import numpy as np
import argparse  

parser = argparse.ArgumentParser(description="Send numbers to BentoML model")
parser.add_argument("numbers", type=float, nargs='+', help="Numbers to input into the model")
args = parser.parse_args()
d = args.numbers
print(f'Which number is bigger, {d[0]} or {d[1]}?')
with bentoml.SyncHTTPClient(
    "http://localhost:3000",
) as client:
    result = client.predict(
        data=d,
    )
    print(result)
    p=np.argmax(result)
    print(f'{d[p]} is bigger ({(result[0][p]*100):3f}% chance)')
    