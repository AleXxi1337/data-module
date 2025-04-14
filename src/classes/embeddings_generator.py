import json
import torch
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity
import pandas as pd

def singleton(cls):
    instances = {}
    
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class EmbeddingGenerator:

    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
        self._device = self._get_device()
        self.model = SentenceTransformer(model_name).to(self._device)
        self.model.eval()

    def _get_device(self):
        if torch.cuda.is_available():
            return torch.device('cuda')
        raise RuntimeError("CUDA is not available. Please check your GPU configuration.")
    
    @torch.no_grad()
    def generate(self, text, batch_size : int = 32) -> torch.Tensor:
        return self.model.encode(
            text,
            convert_to_tensor=True,
            device=self._device,
            batch_size=batch_size,
            normalize_embeddings=True
        )
    
    def embeddings_to_list(self, embeddings : torch.Tensor):
        return embeddings.cpu().tolist()

    def embeddings_from_list(self, embeddings : list):
        return torch.tensor(embeddings).to(self._device)
