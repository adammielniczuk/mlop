import torch.nn as nn
import lightning as L
import torch.nn.functional as F
class Model(L.LightningModule):
    def __init__(self, hidden_size=32,lr=1e-3):
        super().__init__()
        self.save_hyperparameters() 
        self.lr=lr
        self.model=nn.Sequential(nn.Linear(2, hidden_size ),
                                 nn.Tanh(),
                                 nn.Linear(hidden_size, hidden_size),
                                 nn.Tanh(),
                                 nn.Linear(hidden_size,2))
        self.loss_fn = nn.CrossEntropyLoss()
    def forward(self, x):
        return self.model(x)
    

    def predict(self, x):
     
        logits = self(x)
        return F.softmax(logits, dim=1)
