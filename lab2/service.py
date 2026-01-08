import bentoml
import torch
from pathlib import Path
from model import Model

def preprocess_input(values):
    tensor = torch.FloatTensor(values)
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    return tensor

@bentoml.service
class prediction:
    def __init__(self) -> None:
        print("Loading model...")
        MODEL_PATH = Path("best_model.ckpt")
        self.model = Model.load_from_checkpoint(MODEL_PATH, map_location=torch.device('cpu'))
        self.model.eval()
        print("Model loaded successfully!")

    @bentoml.api
    def predict(self, data: list):
        print(f"Received data: {data}") 
        preprocessed_data = preprocess_input(data)
        
        with torch.no_grad(): 
            result = self.model.predict(preprocessed_data)
        
        return result.cpu().detach().numpy().tolist()