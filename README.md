# 📄 DocuMind - RAG-Powered Document Intelligence System

A production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent querying of PDF documents using semantic search and large language models.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.22-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Overview

DocuMind transforms how users interact with document collections by implementing a sophisticated RAG pipeline that combines semantic search with contextual AI responses. Unlike traditional keyword search, this system understands the meaning and context of queries to deliver accurate, source-cited answers.

## ✨ Key Features

### Core Functionality
- **Semantic Document Search**: Advanced embedding-based retrieval using sentence transformers
- **RAG Pipeline**: Retrieval-Augmented Generation for grounded, accurate responses
- **Multi-Document Support**: Process and query multiple PDFs simultaneously
- **Source Attribution**: Every answer includes citations to specific document sections
- **Comparison Mode**: Demonstrates RAG effectiveness vs. non-RAG responses

### Technical Features
- **Vector Database**: ChromaDB for efficient similarity search
- **Embedding Generation**: Sentence-transformers for high-quality text embeddings
- **Chunking Strategy**: Intelligent text splitting with overlap for context preservation
- **Performance Tracking**: Real-time metrics for response time and retrieval quality
- **Export Capabilities**: Save conversations in Markdown and JSON formats

## 🏗️ System Architecture
```
┌─────────────────┐
│  PDF Documents  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   Document Processor         │
│  • Text Extraction           │
│  • Intelligent Chunking      │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Embedding Generator        │
│  • Sentence Transformers     │
│  • Batch Processing          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Vector Store (ChromaDB)    │
│  • Efficient Storage         │
│  • Similarity Search         │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Query Processing           │
│  • Semantic Search           │
│  • Context Retrieval         │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   LLM Response Generation    │
│  • Context-Grounded Answers  │
│  • Source Citations          │
└─────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.10+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/documind.git
cd documind
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment** (Optional - for OpenAI)
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Basic Workflow

1. **Upload Documents**
   - Click "Upload PDFs" in the sidebar
   - Select one or more PDF files
   - Click "Process Documents"

2. **Query Your Documents**
   - Type your question in the chat input
   - Receive contextual answers with source citations
   - View performance metrics

3. **Compare RAG Performance**
   - Switch to "Compare RAG" mode
   - See the difference between RAG and non-RAG responses
   - Understand the value of document-grounded answers

### Advanced Features

**Performance Analytics**
- Navigate to the "Analytics" tab
- View response times, query history, and retrieval statistics

**Export Conversations**
- Go to "Settings" tab
- Export chat history as Markdown or JSON
- Include performance metrics in exports

## 🛠️ Technical Implementation

### Document Processing Pipeline
```python
# Text extraction and chunking
DocumentProcessor()
  ├── extract_text_from_pdf()  # PyPDF2 extraction
  ├── chunk_text()              # Overlapping chunks
  └── process_pdf()             # Complete pipeline
```

**Chunking Strategy:**
- Chunk Size: 1000 characters
- Overlap: 200 characters
- Preserves context across chunk boundaries

### Embedding Generation
```python
# Sentence transformer embeddings
EmbeddingGenerator()
  ├── Model: all-MiniLM-L6-v2
  ├── Dimension: 384
  └── Batch processing for efficiency
```

### Vector Storage & Retrieval
```python
# ChromaDB for similarity search
VectorStore()
  ├── add_documents()     # Store embeddings
  ├── search()            # Semantic retrieval
  └── get_stats()         # Collection metrics
```

**Search Strategy:**
- Cosine similarity for ranking
- Top-K retrieval (default: 3 chunks)
- Distance-based filtering

### LLM Integration
```python
# Flexible LLM support
LLMHandler()
  ├── OpenAI API (with fallback)
  ├── Local model support (Ollama)
  └── Context-aware prompting
```

## 📊 Performance Metrics

The system tracks and displays:
- **Response Time**: End-to-end query processing
- **Retrieval Quality**: Number of relevant chunks
- **Source Attribution**: Documents referenced
- **Query History**: Recent queries with timestamps

## 🎓 Educational Value

This project demonstrates proficiency in:

**Data Science & ML**
- Natural Language Processing (NLP)
- Semantic similarity and embeddings
- Vector databases and similarity search
- Large Language Model (LLM) integration

**Software Engineering**
- Production-ready code architecture
- Error handling and logging
- Performance optimization
- User interface design

**MLOps & Deployment**
- Modular code structure
- Environment management
- Configuration handling
- Metrics tracking

## 🔧 Configuration

Key settings in `src/config.py`:
```python
CHUNK_SIZE = 1000           # Characters per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K_RESULTS = 3           # Chunks to retrieve
LLM_MODEL = "gpt-3.5-turbo" # OpenAI model
```

## 📁 Project Structure
```
documind/
├── app.py                      # Main Streamlit application
├── src/
│   ├── config.py              # Configuration settings
│   ├── document_processor.py  # PDF processing & chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB operations
│   ├── llm_handler.py         # LLM integration
│   ├── comparison.py          # RAG comparison logic
│   ├── metrics.py             # Performance tracking
│   └── export_utils.py        # Export functionality
├── data/
│   ├── uploads/               # Uploaded PDFs
│   └── vectordb/              # ChromaDB storage
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🚧 Future Enhancements

- [ ] Multi-language document support
- [ ] Advanced filtering and metadata search
- [ ] Document comparison features
- [ ] Batch query processing
- [ ] Custom embedding model fine-tuning
- [ ] REST API for programmatic access
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Azure/GCP)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-profile)
- GitHub: [your-github](https://github.com/your-username)
- Email: your.email@example.com

## 🙏 Acknowledgments

- **Streamlit** for the intuitive web framework
- **ChromaDB** for efficient vector storage
- **Sentence-Transformers** for embedding models
- **OpenAI** for LLM capabilities
- **LangChain** community for RAG inspiration

## 📚 References

- [Retrieval-Augmented Generation (RAG) Paper](https://arxiv.org/abs/2005.11401)
- [Sentence-BERT Paper](https://arxiv.org/abs/1908.10084)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**⭐ If you find this project useful, please consider giving it a star!**
