import torch
import torch.nn as nn

device = torch.device(
    0 if torch.cuda.is_available()
    else "cpu"
)

class model(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.mlp = nn.Sequential(
            #first layer
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.5),
            #hidden layer
            nn.Linear(64, 8),
            nn.ReLU(),
            nn.BatchNorm1d(8),
            nn.Dropout(0.5),
            #output scalar score
            nn.Linear(8, 1)
        )

    def forward(self, x):
        return self.mlp(x)
    
embed_to_score = model(input_dim=512)
embed_to_score.load_state_dict(torch.load("./rating/model.pth"))

def embed_to_rating(tensor):
    with torch.no_grad():
        embed_to_score.eval()
        output = embed_to_score(tensor.to(device))
        return output.item()