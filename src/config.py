import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Paths
    UPLOAD_DIR = "data/uploads"
    VECTOR_DB_DIR = "data/vectordb"
    
    # Chunking Parameters
    CHUNK_SIZE = 1000  # characters per chunk
    CHUNK_OVERLAP = 200  # overlap between chunks
    
    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # LLM Parameters
    LLM_MODEL = "gpt-3.5-turbo"  # or "gpt-4" if you have access
    LLM_TEMPERATURE = 0.1  # Low temperature = more focused answers
    MAX_TOKENS = 500
    
    # Retrieval
    TOP_K_RESULTS = 3  # Number of chunks to retrieve
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories if they don't exist"""
        os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
        os.makedirs(Config.VECTOR_DB_DIR, exist_ok=True)