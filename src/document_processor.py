from typing import List, Dict
from PyPDF2 import PdfReader
import os

class DocumentProcessor:
    """Handles PDF processing and text chunking"""
    
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """Extract text from PDF file"""
        try:
            reader = PdfReader(pdf_path)
            text_content = ""
            num_pages = len(reader.pages)
            
            # Extract text from each page
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            # Get metadata
            metadata = {
                "filename": os.path.basename(pdf_path),
                "num_pages": num_pages,
                "file_path": pdf_path
            }
            
            return {
                "text": text_content,
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            return {
                "text": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Split text into chunks with overlap"""
        chunks = []
        words = text.split()
        
        i = 0
        chunk_id = 0
        
        while i < len(words):
            # Take chunk_size words
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Create chunk with metadata
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_id": chunk_id,
                    "total_chunks": "TBD"  # Will update later
                }
            })
            
            # Move forward with overlap
            i += self.chunk_size - self.chunk_overlap
            chunk_id += 1
        
        # Update total_chunks in all chunks
        for chunk in chunks:
            chunk["metadata"]["total_chunks"] = len(chunks)
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """Complete processing pipeline for a PDF"""
        # Extract text
        extraction_result = self.extract_text_from_pdf(pdf_path)
        
        if not extraction_result["success"]:
            return extraction_result
        
        # Chunk text
        chunks = self.chunk_text(
            extraction_result["text"],
            extraction_result["metadata"]
        )
        
        return {
            "success": True,
            "chunks": chunks,
            "metadata": extraction_result["metadata"],
            "num_chunks": len(chunks)
        }








# from typing import List, Dict
# from PyPDF2 import PdfReader # type: ignore
# from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
# from src.config import Config # type: ignore
# import os

# class DocumentProcessor:
#     """Handles PDF processing and text chunking"""
    
#     def __init__(self):
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=Config.CHUNK_SIZE,
#             chunk_overlap=Config.CHUNK_OVERLAP,
#             length_function=len,
#             separators=["\n\n", "\n", ". ", " ", ""]
#         )
    
#     def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, any]:
#         """
#         Extract text from PDF file
        
#         Args:
#             pdf_path: Path to PDF file
            
#         Returns:
#             Dictionary with text content and metadata
#         """
#         try:
#             reader = PdfReader(pdf_path)
            
#             text_content = ""
#             num_pages = len(reader.pages)
            
#             # Extract text from each page
#             for page_num, page in enumerate(reader.pages):
#                 page_text = page.extract_text()
#                 text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
#             # Get metadata
#             metadata = {
#                 "filename": os.path.basename(pdf_path),
#                 "num_pages": num_pages,
#                 "file_path": pdf_path
#             }
            
#             return {
#                 "text": text_content,
#                 "metadata": metadata,
#                 "success": True
#             }
            
#         except Exception as e:
#             return {
#                 "text": "",
#                 "metadata": {},
#                 "success": False,
#                 "error": str(e)
#             }
    
#     def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
#         """
#         Split text into chunks with metadata
        
#         Args:
#             text: Full text content
#             metadata: Document metadata
            
#         Returns:
#             List of chunks with metadata
#         """
#         # Split text into chunks
#         chunks = self.text_splitter.split_text(text)
        
#         # Add metadata to each chunk
#         chunks_with_metadata = []
#         for i, chunk in enumerate(chunks):
#             chunk_data = {
#                 "content": chunk,
#                 "metadata": {
#                     **metadata,
#                     "chunk_id": i,
#                     "total_chunks": len(chunks)
#                 }
#             }
#             chunks_with_metadata.append(chunk_data)
        
#         return chunks_with_metadata
    
#     def process_pdf(self, pdf_path: str) -> Dict:
#         """
#         Complete processing pipeline for a PDF
        
#         Args:
#             pdf_path: Path to PDF file
            
#         Returns:
#             Processing results with chunks
#         """
#         # Extract text
#         extraction_result = self.extract_text_from_pdf(pdf_path)
        
#         if not extraction_result["success"]:
#             return extraction_result
        
#         # Chunk text
#         chunks = self.chunk_text(
#             extraction_result["text"],
#             extraction_result["metadata"]
#         )
        
#         return {
#             "success": True,
#             "chunks": chunks,
#             "metadata": extraction_result["metadata"],
#             "num_chunks": len(chunks)
#         }