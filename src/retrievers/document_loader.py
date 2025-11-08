"""
Document loading and chunking utilities
"""

import os
from glob import glob
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config import Config


@dataclass
class DocChunk:
    """Represents a chunk of a document with metadata"""
    page_content: str
    metadata: Dict[str, Any]


class DocumentLoader:
    """Handles loading and chunking of PDF documents"""
    
    def __init__(
        self,
        chunk_size: int = Config.CHUNK_SIZE,
        chunk_overlap: int = Config.CHUNK_OVERLAP
    ):
        """
        Initialize document loader.
        
        Args:
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_and_chunk_pdfs(self, files_dir: str) -> List[DocChunk]:
        """
        Load all PDFs from a directory and chunk them.
        
        Args:
            files_dir: Directory containing PDF files
            
        Returns:
            List of document chunks with metadata
        """
        chunks: List[DocChunk] = []
        pdf_paths = sorted(glob(os.path.join(files_dir, "*.pdf")))
        
        if not pdf_paths:
            print(f"⚠️  No PDF files found in {files_dir}")
            return chunks
        
        for pdf_path in pdf_paths:
            filename = os.path.basename(pdf_path)
            try:
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()
            except Exception as e:
                print(f"⚠️  Failed to load {pdf_path}: {e}")
                continue
            
            # Add metadata to each document
            for i, d in enumerate(docs):
                if not d.metadata:
                    d.metadata = {}
                d.metadata["source"] = filename
                d.metadata["orig_page_index"] = d.metadata.get("page", i)
            
            # Split documents into chunks
            doc_chunks = self.splitter.split_documents(docs)
            
            # Add chunk IDs and convert to DocChunk
            for idx, c in enumerate(doc_chunks):
                meta = dict(c.metadata)
                meta["chunk_id"] = f"{filename}__chunk{idx}"
                chunks.append(
                    DocChunk(page_content=c.page_content, metadata=meta)
                )
        
        print(f"📚 Loaded and chunked {len(chunks)} chunks from {len(pdf_paths)} PDF(s).")
        return chunks
