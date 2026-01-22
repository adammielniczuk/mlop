import json
import boto3
import os
import joblib
import numpy as np
from PIL import Image
import io

s3 = boto3.client('s3')

model_path = os.environ.get('MODEL_PATH', 'model.joblib')
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

def get_prediction(image_bytes):
    if model is None:
        raise Exception("Model not loaded")

    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((28, 28)).convert('L')
    img_data = np.array(img)
    
    img_data = img_data / 255.0

    img_data = img_data.reshape(1, -1)
    
    prediction = model.predict(img_data)
    return int(prediction[0])

def handler(event, context):
    
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        digit = get_prediction(file_content)
        result_key = f"results/{os.path.basename(key)}.json"
        result_body = json.dumps({'digit': digit, 'source_image': key})
        
        s3.put_object(Bucket=bucket, Key=result_key, Body=result_body)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Inference successful')
        }
        
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
