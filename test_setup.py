import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
print(f"Python path: {sys.path[0]}")
print(f"Current directory: {os.getcwd()}")

try:
    from src.config import Config
    print("✓ Config imported")
    
    from src.document_processor import DocumentProcessor
    print("✓ DocumentProcessor imported")
    
    from src.embeddings import EmbeddingGenerator
    print("✓ EmbeddingGenerator imported")
    
    from src.vector_store import VectorStore
    print("✓ VectorStore imported")
    
    from src.llm_handler import LLMHandler
    print("✓ LLMHandler imported")
    
    print("\n" + "="*50)
    print("✓✓✓ ALL IMPORTS SUCCESSFUL! ✓✓✓")
    print("="*50)
    
    Config.ensure_directories()
    print("\n✓ Directories created successfully")
    print("\n🎉 Setup complete! Ready to build!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()





# print("Testing imports...")

# try:
#     from src.config import Config # pyright: ignore[reportMissingImports]
#     print("✓ Config imported")
    
#     from src.document_processor import DocumentProcessor
#     print("✓ DocumentProcessor imported")
    
#     from src.embeddings import EmbeddingGenerator
#     print("✓ EmbeddingGenerator imported")
    
#     from src.vector_store import VectorStore
#     print("✓ VectorStore imported")
    
#     from src.llm_handler import LLMHandler
#     print("✓ LLMHandler imported")
    
#     print("\n" + "="*50)
#     print("✓✓✓ ALL IMPORTS SUCCESSFUL! ✓✓✓")
#     print("="*50)
    
#     # Test directory creation
#     Config.ensure_directories()
#     print("\n✓ Directories created successfully")
    
#     print("\n🎉 Setup complete! Ready to build!")
    
# except Exception as e:
#     print(f"\n❌ Error: {e}")
#     print("\nPlease check:")
#     print("1. Virtual environment is activated (venv)")
#     print("2. All packages installed (pip install -r requirements.txt)")
#     print("3. All files saved properly")