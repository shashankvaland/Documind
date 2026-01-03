from sentence_transformers import SentenceTransformer # pyright: ignore[reportMissingImports]
from typing import List
import numpy as np # pyright: ignore[reportMissingImports]
from src.config import Config # pyright: ignore[reportMissingImports]

class EmbeddingGenerator:
    """Generates embeddings for text chunks"""
    
    def __init__(self):
        print(f"Loading embedding model: {Config.EMBEDDING_MODEL}")
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        print("✓ Embedding model loaded successfully")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts (more efficient)
        
        Args:
            texts: List of input texts
            
        Returns:
            Array of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        return self.model.get_sentence_embedding_dimension()