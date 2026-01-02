import streamlit as st
import os
import time
from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.llm_handler import LLMHandler
from src.comparison import RAGComparison
from src.metrics import PerformanceMetrics
from src.export_utils import ExportUtils

# Page configuration
st.set_page_config(
    page_title="DocuMind - Intelligent Document Query",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .performance-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "llm_handler" not in st.session_state:
    st.session_state.llm_handler = None
if "comparison_mode" not in st.session_state:
    st.session_state.comparison_mode = False
if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0
if "metrics" not in st.session_state:
    st.session_state.metrics = PerformanceMetrics()
if "show_metrics" not in st.session_state:
    st.session_state.show_metrics = False

Config.ensure_directories()

# Header
st.markdown('<div class="main-header">📚 DocuMind</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">RAG-Powered Document Intelligence System</div>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Analytics", "⚙️ Settings"])

with tab3:
    st.header("⚙️ Settings & Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Display Options")
        show_sources = st.checkbox("Show sources in chat", value=True)
        show_timestamps = st.checkbox("Show timestamps", value=False)
        
        st.subheader("🔧 System Info")
        st.info(f"""
        **Embedding Model:** {Config.EMBEDDING_MODEL}
        **Chunk Size:** {Config.CHUNK_SIZE} characters
        **Chunk Overlap:** {Config.CHUNK_OVERLAP} characters
        **Top-K Results:** {Config.TOP_K_RESULTS}
        """)
    
    with col2:
        st.subheader("📥 Export Data")
        
        if st.session_state.messages:
            # Export to Markdown
            if st.button("📄 Export Chat (Markdown)", use_container_width=True):
                md_content = ExportUtils.export_chat_to_markdown(
                    st.session_state.messages,
                    st.session_state.documents_processed
                )
                st.download_button(
                    label="⬇️ Download Markdown",
                    data=md_content,
                    file_name=f"documind_chat_{time.strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
            
            # Export to JSON
            if st.button("📊 Export Chat (JSON)", use_container_width=True):
                json_content = ExportUtils.export_chat_to_json(
                    st.session_state.messages,
                    st.session_state.documents_processed,
                    st.session_state.metrics.get_summary_stats()
                )
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_content,
                    file_name=f"documind_chat_{time.strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        else:
            st.info("💡 Start a conversation to enable export options")

with tab2:
    st.header("📊 Performance Analytics")
    
    if st.session_state.metrics.get_total_queries() > 0:
        stats = st.session_state.metrics.get_summary_stats()
        
        # Metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_queries']}</div>
                <div class="metric-label">Total Queries</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['avg_response_time']:.2f}s</div>
                <div class="metric-label">Avg Response Time</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['fastest_query']:.2f}s</div>
                <div class="metric-label">Fastest Query</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_chunks_retrieved']}</div>
                <div class="metric-label">Chunks Retrieved</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recent queries
        st.subheader("📝 Recent Query History")
        recent = st.session_state.metrics.get_recent_queries(10)
        
        for i, query_data in enumerate(reversed(recent), 1):
            with st.expander(f"Query {i}: {query_data['query'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Response Time", f"{query_data['response_time']:.2f}s")
                with col2:
                    st.metric("Chunks Retrieved", query_data['num_chunks_retrieved'])
                with col3:
                    st.metric("Sources Used", query_data['num_sources'])
                
                st.text(f"Timestamp: {query_data['timestamp']}")
    else:
        st.info("📊 Analytics will appear here after you start querying documents")

with tab1:
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Mode selector
        st.markdown("### 🎯 Query Mode")
        mode = st.radio(
            "Choose mode:",
            ["💬 Normal Chat", "⚖️ Compare RAG vs No RAG"],
            label_visibility="collapsed"
        )
        st.session_state.comparison_mode = (mode == "⚖️ Compare RAG vs No RAG")
        
        st.markdown("---")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload PDF Documents",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to query"
        )
        
        # Process documents
        if uploaded_files:
            if st.button("🔄 Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    try:
                        processor = DocumentProcessor()
                        
                        if st.session_state.vector_store is None:
                            st.session_state.vector_store = VectorStore()
                        
                        if st.session_state.llm_handler is None:
                            st.session_state.llm_handler = LLMHandler()
                        
                        all_chunks = []
                        
                        progress_bar = st.progress(0)
                        for idx, uploaded_file in enumerate(uploaded_files):
                            file_path = os.path.join(Config.UPLOAD_DIR, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            st.info(f"📄 Processing: {uploaded_file.name}")
                            result = processor.process_pdf(file_path)
                            
                            if result["success"]:
                                all_chunks.extend(result["chunks"])
                                st.session_state.documents_processed.append({
                                    "name": uploaded_file.name,
                                    "chunks": result["num_chunks"],
                                    "pages": result["metadata"]["num_pages"]
                                })
                                st.success(f"✓ {uploaded_file.name}: {result['num_chunks']} chunks")
                            else:
                                st.error(f"✗ Error: {result.get('error', 'Unknown')}")
                            
                            progress_bar.progress((idx + 1) / len(uploaded_files))
                        
                        if all_chunks:
                            st.info("🔄 Creating embeddings...")
                            store_result = st.session_state.vector_store.add_documents(all_chunks)
                            
                            if store_result["success"]:
                                st.session_state.total_chunks += len(all_chunks)
                                st.success(f"🎉 Successfully processed {len(all_chunks)} chunks!")
                                st.balloons()
                            else:
                                st.error(f"Error: {store_result.get('error', 'Unknown')}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Statistics
        if st.session_state.documents_processed:
            st.markdown("---")
            st.markdown("### 📊 Quick Stats")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(st.session_state.documents_processed)}</div>
                    <div class="metric-label">Documents</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{st.session_state.total_chunks}</div>
                    <div class="metric-label">Chunks</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("📄 Documents")
            for doc in st.session_state.documents_processed:
                with st.expander(f"📄 {doc['name']}"):
                    st.write(f"**Pages:** {doc['pages']}")
                    st.write(f"**Chunks:** {doc['chunks']}")
        
        # Clear button
        if st.session_state.documents_processed:
            st.markdown("---")
            if st.button("🗑️ Clear All", type="secondary"):
                st.session_state.documents_processed = []
                st.session_state.messages = []
                st.session_state.vector_store = None
                st.session_state.llm_handler = None
                st.session_state.total_chunks = 0
                st.session_state.metrics = PerformanceMetrics()
                st.rerun()
    
    # Main chat area
    st.markdown("---")
    
    if not st.session_state.documents_processed:
        # Welcome screen
        st.info("👈 **Get Started:** Upload PDF documents in the sidebar to begin!")
        
        st.markdown("### ✨ Key Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🔍 Semantic Search
            - Advanced embedding-based search
            - Context-aware retrieval
            - Finds relevant info instantly
            """)
        
        with col2:
            st.markdown("""
            #### 🤖 AI-Powered Q&A
            - Grounded in your documents
            - Source citations included
            - Accurate contextual answers
            """)
        
        with col3:
            st.markdown("""
            #### 📊 Performance Tracking
            - Response time metrics
            - Query analytics
            - Export capabilities
            """)
    
    else:
        # Chat interface
        if st.session_state.comparison_mode:
            st.subheader("⚖️ Compare: RAG vs No RAG")
            st.info("💡 See the difference between answers WITH and WITHOUT document access!")
        else:
            st.subheader("💬 Chat with Your Documents")
        
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                if show_sources and "sources" in message and message["sources"]:
                    with st.expander("📎 View Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:** {source.get('filename', 'Unknown')}")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            start_time = time.time()
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        if st.session_state.comparison_mode:
                            comparison = RAGComparison(
                                st.session_state.llm_handler,
                                st.session_state.vector_store
                            )
                            result = comparison.compare_answers(prompt)
                            
                            st.markdown("### 🚫 Without RAG")
                            st.markdown(result["without_rag"]["answer"])
                            st.markdown("---")
                            st.markdown("### ✅ With RAG")
                            st.markdown(result["with_rag"]["answer"])
                            
                            if result["with_rag"]["sources"]:
                                with st.expander("📎 Sources Used"):
                                    for i, source in enumerate(result["with_rag"]["sources"], 1):
                                        st.markdown(f"**{i}.** {source.get('filename', 'Unknown')}")
                            
                            answer = "Comparison complete! See above for differences."
                            sources = result["with_rag"]["sources"]
                            num_chunks = len(sources)
                        
                        else:
                            relevant_chunks = st.session_state.vector_store.search(prompt, top_k=Config.TOP_K_RESULTS)
                            result = st.session_state.llm_handler.generate_answer(prompt, relevant_chunks)
                            
                            if result["success"]:
                                answer = result["answer"]
                                st.markdown(answer)
                                
                                if show_sources and "sources" in result and result["sources"]:
                                    with st.expander("📎 View Sources"):
                                        for i, source in enumerate(result["sources"], 1):
                                            st.markdown(f"**Source {i}:** {source.get('filename', 'Unknown')}")
                            else:
                                answer = f"Error: {result.get('error', 'Unknown error')}"
                                st.error(answer)
                            
                            sources = result.get("sources", [])
                            num_chunks = len(relevant_chunks)
                        
                        # Track metrics
                        response_time = time.time() - start_time
                        st.session_state.metrics.track_query(
                            prompt,
                            response_time,
                            num_chunks,
                            sources
                        )
                        
                        # Show performance info
                        st.caption(f"⚡ Response time: {response_time:.2f}s | Chunks: {num_chunks}")
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                    
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 1rem;'>
    <p><strong>DocuMind v1.0</strong> - RAG-Powered Document Intelligence</p>
    <p style='font-size: 0.85rem;'>Streamlit • ChromaDB • Sentence Transformers • OpenAI</p>
</div>
""", unsafe_allow_html=True)