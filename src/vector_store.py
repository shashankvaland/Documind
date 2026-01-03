import chromadb # pyright: ignore[reportMissingImports]
from chromadb.config import Settings # pyright: ignore[reportMissingImports]
from typing import List, Dict
import uuid
from src.config import Config # pyright: ignore[reportMissingImports]
from src.embeddings import EmbeddingGenerator

class VectorStore:
    """Manages ChromaDB vector database for document chunks"""
    
    def __init__(self, collection_name: str = "documents"):
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=Config.VECTOR_DB_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Document chunks with embeddings"}
        )
        
        print(f"✓ Vector store initialized. Collection: {collection_name}")
    
    def add_documents(self, chunks: List[Dict]) -> Dict:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of chunks with content and metadata
            
        Returns:
            Status dictionary
        """
        try:
            # Extract texts
            texts = [chunk["content"] for chunk in chunks]
            
            # Generate embeddings
            print(f"Generating embeddings for {len(texts)} chunks...")
            embeddings = self.embedding_generator.generate_embeddings_batch(texts)
            
            # Prepare data for ChromaDB
            ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
            metadatas = [chunk["metadata"] for chunk in chunks]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=texts,
                metadatas=metadatas
            )
            
            print(f"✓ Added {len(chunks)} chunks to vector store")
            
            return {
                "success": True,
                "num_chunks_added": len(chunks),
                "collection_size": self.collection.count()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for relevant chunks using semantic similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with metadata
        """
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        return {
            "total_chunks": self.collection.count(),
            "collection_name": self.collection.name
        }
    
    def clear_collection(self):
        """Clear all documents from collection"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            metadata={"description": "Document chunks with embeddings"}
        )
        print("✓ Collection cleared")
    
    