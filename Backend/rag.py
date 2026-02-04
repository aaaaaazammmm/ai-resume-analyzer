"""
RAG (Retrieval Augmented Generation) module using FAISS
"""
import os
import re
from typing import List, Tuple
import faiss
import numpy as np
from embeddings import get_embedding_service


class DocumentChunker:
    """Utility for chunking documents"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\(\)\:\;]', '', text)
        return text.strip()
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text
            chunk_size: Maximum characters per chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        text = DocumentChunker.clean_text(text)
        words = text.split()
        
        if len(words) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunks.append(' '.join(chunk_words))
            start = end - overlap
        
        return chunks


class VectorStore:
    """FAISS-based vector store for document retrieval"""
    
    def __init__(self):
        """Initialize vector store"""
        self.embedding_service = get_embedding_service()
        self.dimension = self.embedding_service.embedding_dim
        self.index = None
        self.documents = []
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index"""
        # Use L2 distance for similarity
        self.index = faiss.IndexFlatL2(self.dimension)
        print(f"FAISS index initialized with dimension {self.dimension}")
    
    def add_documents(self, documents: List[str]):
        """
        Add documents to vector store
        
        Args:
            documents: List of document chunks
        """
        if not documents:
            return
        
        self.documents.extend(documents)
        
        # Generate embeddings
        embeddings = self.embedding_service.embed_documents(documents)
        
        if embeddings.size > 0:
            # Add to FAISS index
            self.index.add(embeddings.astype('float32'))
            print(f"Added {len(documents)} documents to vector store")
    
    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for similar documents
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (document, distance) tuples
        """
        if not self.documents or self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_text(query)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        k = min(k, len(self.documents))
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(dist)))
        
        return results
    
    def clear(self):
        """Clear all documents and reset index"""
        self.documents = []
        self._initialize_index()


class RAGService:
    """Main RAG service for resume analysis"""
    
    def __init__(self):
        """Initialize RAG service"""
        self.vector_store = VectorStore()
        self.chunker = DocumentChunker()
    
    def process_resume(self, resume_text: str) -> str:
        """
        Process resume and add to vector store
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Cleaned resume text
        """
        # Clean text
        cleaned_text = self.chunker.clean_text(resume_text)
        
        # Chunk text
        chunks = self.chunker.chunk_text(cleaned_text, chunk_size=300, overlap=50)
        
        # Clear previous data and add new chunks
        self.vector_store.clear()
        self.vector_store.add_documents(chunks)
        
        return cleaned_text
    
    def retrieve_relevant_context(self, job_description: str, k: int = 5) -> str:
        """
        Retrieve relevant resume sections based on job description
        
        Args:
            job_description: Job description text
            k: Number of chunks to retrieve
            
        Returns:
            Concatenated relevant context
        """
        results = self.vector_store.search(job_description, k=k)
        
        if not results:
            return ""
        
        # Combine top results
        context_chunks = [doc for doc, _ in results]
        return " ".join(context_chunks)


# Global instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get or create global RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
