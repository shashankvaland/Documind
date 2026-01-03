from typing import List, Dict
import json
from datetime import datetime

class ExportUtils:
    """Utility functions for exporting data"""
    
    @staticmethod
    def export_chat_to_markdown(messages: List[Dict], documents: List[Dict]) -> str:
        """Export chat history to markdown format"""
        
        md_content = f"""# DocuMind Chat Export
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Documents Processed
"""
        
        for doc in documents:
            md_content += f"- **{doc['name']}** ({doc['pages']} pages, {doc['chunks']} chunks)\n"
        
        md_content += "\n---\n\n## Conversation\n\n"
        
        for msg in messages:
            role = "🧑 **You:**" if msg["role"] == "user" else "🤖 **DocuMind:**"
            md_content += f"{role}\n{msg['content']}\n\n"
            
            if "sources" in msg and msg["sources"]:
                md_content += "**Sources:**\n"
                for source in msg["sources"]:
                    md_content += f"- {source.get('filename', 'Unknown')}\n"
                md_content += "\n"
            
            md_content += "---\n\n"
        
        return md_content
    
    @staticmethod
    def export_chat_to_json(messages: List[Dict], documents: List[Dict], metrics: Dict = None) -> str:
        """Export chat history to JSON format"""
        
        export_data = {
            "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "documents": documents,
            "conversation": messages,
            "metrics": metrics or {}
        }
        
        return json.dumps(export_data, indent=2)