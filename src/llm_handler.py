from typing import List, Dict
from openai import OpenAI
from src.config import Config

class LLMHandler:
    """Handles LLM interactions for generating answers"""
    
    def __init__(self):
        if Config.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.use_openai = True
                print("✓ OpenAI client initialized")
            except:
                self.use_openai = False
                print("⚠ OpenAI initialization failed - using fallback mode")
        else:
            self.use_openai = False
            print("⚠ No OpenAI API key found - using fallback mode")
    
    def create_prompt(self, query: str, context_chunks: List[Dict]) -> str:
        """Create prompt with context from retrieved chunks"""
        context = "\n\n".join([
            f"[Source: {chunk['metadata']['filename']}]\n{chunk['content']}"
            for chunk in context_chunks
        ])
        
        prompt = f"""Context from documents:
{context}

Question: {query}

Answer based only on the context above:"""
        return prompt
    
    def generate_answer(self, query: str, context_chunks: List[Dict]) -> Dict:
        """Generate answer using LLM with retrieved context"""
        
        # Always try fallback first if no OpenAI or quota exceeded
        if not self.use_openai:
            return self._fallback_answer(query, context_chunks)
        
        try:
            # Create prompt
            prompt = self.create_prompt(query, context_chunks)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on document context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.LLM_TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )
            
            answer = response.choices[0].message.content
            
            return {
                "success": True,
                "answer": answer,
                "sources": [chunk['metadata'] for chunk in context_chunks],
                "model": Config.LLM_MODEL
            }
            
        except Exception as e:
            # If OpenAI fails (quota, network, etc.), use fallback
            print(f"OpenAI error: {str(e)}")
            print("Falling back to direct document retrieval...")
            return self._fallback_answer(query, context_chunks)
    
    def _fallback_answer(self, query: str, context_chunks: List[Dict]) -> Dict:
        """
        Fallback when no LLM API available
        Returns relevant chunks formatted nicely
        """
        if not context_chunks:
            answer = "❌ No relevant information found in the documents for your query."
        else:
            # Create a nice summary from retrieved chunks
            answer = "📄 **Here's what I found in your documents:**\n\n"
            
            for i, chunk in enumerate(context_chunks, 1):
                source = chunk['metadata'].get('filename', 'Unknown')
                content = chunk['content'][:500]  # First 500 chars
                
                answer += f"**Excerpt {i}** (from *{source}*):\n"
                answer += f"{content}...\n\n"
            
            answer += "\n💡 *Note: Using direct document retrieval mode. Add OpenAI API credits for AI-generated summaries.*"
        
        return {
            "success": True,
            "answer": answer,
            "sources": [chunk['metadata'] for chunk in context_chunks],
            "model": "fallback-retrieval"
        }


















# from typing import List, Dict
# from openai import OpenAI # pyright: ignore[reportMissingImports]
# from src.config import Config # pyright: ignore[reportMissingImports]

# class LLMHandler:
#     """Handles LLM interactions for generating answers"""
    
#     def __init__(self):
#         if Config.OPENAI_API_KEY:
#             self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
#             self.use_openai = True
#             print("✓ OpenAI client initialized")
#         else:
#             self.use_openai = False
#             print("⚠ No OpenAI API key found. Using fallback mode.")
    
#     def create_prompt(self, query: str, context_chunks: List[Dict]) -> str:
#         """
#         Create prompt with context from retrieved chunks
        
#         Args:
#             query: User question
#             context_chunks: Retrieved relevant chunks
            
#         Returns:
#             Formatted prompt
#         """
#         # Combine context from chunks
#         context = "\n\n".join([
#             f"[Source: {chunk['metadata']['filename']}, "
#             f"Page info: Chunk {chunk['metadata']['chunk_id']+1}/"
#             f"{chunk['metadata']['total_chunks']}]\n{chunk['content']}"
#             for chunk in context_chunks
#         ])
        
#         prompt = f"""You are a helpful AI assistant that answers questions based on provided document context.

# Context from documents:
# {context}

# Question: {query}

# Instructions:
# 1. Answer the question using ONLY the information from the context above
# 2. If the context doesn't contain enough information, say so clearly
# 3. Cite which source document you're referencing
# 4. Be concise but complete
# 5. If there are multiple perspectives in the documents, mention them

# Answer:"""
        
#         return prompt
    
#     def generate_answer(self, query: str, context_chunks: List[Dict]) -> Dict:
#         """
#         Generate answer using LLM with retrieved context
        
#         Args:
#             query: User question
#             context_chunks: Retrieved relevant chunks
            
#         Returns:
#             Dictionary with answer and metadata
#         """
#         if not self.use_openai:
#             return self._fallback_answer(query, context_chunks)
        
#         try:
#             # Create prompt
#             prompt = self.create_prompt(query, context_chunks)
            
#             # Call OpenAI API
#             response = self.client.chat.completions.create(
#                 model=Config.LLM_MODEL,
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant that answers questions based on document context."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=Config.LLM_TEMPERATURE,
#                 max_tokens=Config.MAX_TOKENS
#             )
            
#             answer = response.choices[0].message.content
            
#             return {
#                 "success": True,
#                 "answer": answer,
#                 "sources": [chunk['metadata'] for chunk in context_chunks],
#                 "model": Config.LLM_MODEL
#             }
            
#         except Exception as e:
#             return {
#                 "success": False,
#                 "error": str(e),
#                 "answer": "Error generating answer. Please check your API key and try again."
#             }
    
#     def _fallback_answer(self, query: str, context_chunks: List[Dict]) -> Dict:
#         """
#         Fallback when no LLM API available (for testing)
#         Returns the most relevant chunk as answer
#         """
#         if not context_chunks:
#             answer = "No relevant information found in the documents."
#         else:
#             # Return most relevant chunk
#             answer = f"Based on the documents:\n\n{context_chunks[0]['content']}\n\n"
#             answer += f"(Source: {context_chunks[0]['metadata']['filename']})"
        
#         return {
#             "success": True,
#             "answer": answer,
#             "sources": [chunk['metadata'] for chunk in context_chunks],
#             "model": "fallback"
#         }