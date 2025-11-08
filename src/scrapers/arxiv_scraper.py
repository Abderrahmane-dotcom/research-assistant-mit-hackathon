"""
ArXiv article scraper with PDF download capabilities
"""

import io
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None


class ArxivScraper:
    """Scraper for arXiv academic papers"""
    
    def __init__(self):
        """Initialize ArXiv scraper"""
        self.api_url = "http://export.arxiv.org/api/query"
    
    @staticmethod
    def extract_pdf_content(pdf_data: bytes) -> str:
        """
        Extract text content from PDF bytes.
        
        Args:
            pdf_data: PDF file content as bytes
            
        Returns:
            Extracted text from the PDF
        """
        if PdfReader is None:
            return "[PDF content extraction unavailable - pypdf not installed]"
        
        try:
            pdf_file = io.BytesIO(pdf_data)
            reader = PdfReader(pdf_file)
            
            text_content = []
            for page_num, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                except Exception as e:
                    print(f"   ⚠️  Could not extract text from page {page_num + 1}: {e}")
            
            full_text = "\n\n".join(text_content)
            return full_text if full_text.strip() else "[No text could be extracted from PDF]"
        
        except Exception as e:
            return f"[Error extracting PDF content: {e}]"
    
    def scrape_articles(
        self,
        query: str = "ai for climate",
        max_results: int = 5,
        save_pdf: bool = False,
        extract_content: bool = True,
        output_folder: str = "pdfs",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: str = "relevance"
    ) -> List[Dict]:
        """
        Scrape articles from arXiv based on keywords.
        
        Args:
            query: Search keywords
            max_results: Maximum number of papers to retrieve
            save_pdf: Whether to download and save PDFs
            extract_content: Whether to extract text content from PDFs
            output_folder: Folder to save PDFs
            start_date: Filter papers from this date (YYYY-MM-DD)
            end_date: Filter papers until this date (YYYY-MM-DD)
            sort_by: Sort results by 'relevance', 'updated', or 'submitted'
            
        Returns:
            List of dictionaries containing article information
        """
        # Create output folder only if saving PDFs
        if save_pdf:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        # Build arXiv API URL
        url = f"{self.api_url}?search_query={query}&max_results={max_results}"
        
        # Add sorting parameter
        sort_options = {
            "relevance": "relevance",
            "updated": "lastUpdatedDate",
            "submitted": "submittedDate"
        }
        if sort_by in sort_options:
            url += f"&sortBy={sort_options[sort_by]}&sortOrder=descending"
        
        # Query arXiv API
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "xml")
        
        entries = soup.find_all("entry")
        print(f"📄 Found {len(entries)} papers for query: '{query}'")
        
        articles = []
        
        for i, entry in enumerate(entries, 1):
            # Get paper details
            title = entry.title.text.strip().replace('\n', ' ')
            paper_id = entry.id.text.split('/')[-1]
            
            # Get publication date
            published = entry.published.text
            pub_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
            
            # Filter by date range if specified
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                if pub_date < start:
                    print(f"⏭️  Skipping (before {start_date}): {title[:60]}...")
                    continue
            
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if pub_date > end:
                    print(f"⏭️  Skipping (after {end_date}): {title[:60]}...")
                    continue
            
            # Construct PDF URL
            pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
            
            # Get abstract
            abstract = entry.summary.text.strip().replace('\n', ' ') if entry.summary else ""
            
            # Get authors
            authors = [
                author.find('name').text 
                for author in entry.find_all('author')
            ] if entry.find_all('author') else []
            
            article_data = {
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "pdf_url": pdf_url,
                "published": pub_date.strftime('%Y-%m-%d'),
                "arxiv_id": paper_id,
                "content": None,
                "local_path": None
            }
            
            # Download PDF if requested OR if content extraction is needed
            pdf_data = None
            if save_pdf or extract_content:
                print(f"[{i}/{len(entries)}] Downloading: {title[:80]}...")
                try:
                    pdf_response = requests.get(pdf_url)
                    pdf_response.raise_for_status()
                    pdf_data = pdf_response.content
                    
                    # Save to file if requested
                    if save_pdf:
                        safe_title = "".join(
                            c for c in title 
                            if c.isalnum() or c in (' ', '-', '_')
                        ).strip()
                        safe_title = safe_title[:100]
                        filename = f"{i}_{safe_title}.pdf"
                        filepath = os.path.join(output_folder, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(pdf_data)
                        
                        print(f"   ✓ Saved to: {filepath}")
                        article_data["local_path"] = filepath
                    
                    # Extract content if requested
                    if extract_content and pdf_data:
                        print(f"   📖 Extracting content...")
                        content = self.extract_pdf_content(pdf_data)
                        article_data["content"] = content
                        print(f"   ✓ Extracted {len(content)} characters")
                        
                except Exception as e:
                    print(f"   ✗ Failed to download: {e}")
            else:
                print(f"[{i}/{len(entries)}] {title[:80]}...")
            
            articles.append(article_data)
        
        if save_pdf:
            downloaded_count = sum(1 for a in articles if a.get("local_path"))
            print(f"\n✅ {downloaded_count}/{len(articles)} PDFs downloaded successfully!")
        
        if extract_content:
            extracted_count = sum(
                1 for a in articles 
                if a.get("content") and not a.get("content", "").startswith("[")
            )
            print(f"✅ Extracted content from {extracted_count}/{len(articles)} articles")
        
        if not save_pdf and not extract_content:
            print(f"\n✅ {len(articles)} articles retrieved successfully!")
        
        return articles
