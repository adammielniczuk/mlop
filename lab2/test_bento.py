import bentoml

with bentoml.SyncHTTPClient(
    "https://prediction-e705-e944bcd0.mt-guc1.bentoml.ai",
) as client:
    result = client.predict(
        data=[10.0, 5.0],
    )
    print(result)
    