"""
Wikipedia article scraper
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional

from ..utils.text_utils import clean_query_for_wiki


class WikipediaScraper:
    """Scraper for Wikipedia articles"""
    
    def __init__(self, user_agent: str = "WikipediaScraperBot/1.0"):
        """
        Initialize Wikipedia scraper.
        
        Args:
            user_agent: User agent string for requests
        """
        self.headers = {'User-Agent': user_agent}
        self.search_url = "https://en.wikipedia.org/w/api.php"
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, str]]:
        """
        Search Wikipedia and return article titles and URLs.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of tuples (title, url)
        """
        params = {
            "action": "opensearch",
            "search": query,
            "limit": limit,
            "format": "json"
        }
        
        try:
            response = requests.get(
                self.search_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            titles = data[1]
            urls = data[3]
            
            return list(zip(titles, urls))
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching Wikipedia: {e}")
            return []
    
    def scrape_article(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Scrape content from a Wikipedia article.
        
        Args:
            url: Article URL
            
        Returns:
            Tuple of (title, content) or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get title
            title_elem = soup.find('h1', {'id': 'firstHeading'})
            if not title_elem:
                return None
            title = title_elem.text
            
            # Get main content
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if not content_div:
                return title, ""
            
            # Remove unwanted elements
            for unwanted in content_div.find_all(
                ['table', 'div', 'sup', 'span'],
                {'class': ['infobox', 'navbox', 'reference', 'mw-editsection']}
            ):
                unwanted.decompose()
            
            # Extract paragraphs
            paragraphs = content_div.find_all('p')
            text = '\n\n'.join([
                p.get_text().strip() 
                for p in paragraphs 
                if p.get_text().strip()
            ])
            
            return title, text
        
        except Exception as e:
            print(f"   ❌ Error scraping article: {e}")
            return None
    
    def scrape_by_keywords(
        self,
        keywords: str,
        max_articles: int = 5
    ) -> List[Dict[str, str]]:
        """
        Search and scrape Wikipedia articles by keywords.
        
        Args:
            keywords: Search keywords
            max_articles: Maximum number of articles to scrape
            
        Returns:
            List of article dictionaries with title, content, and url
        """
        cleaned_keywords = clean_query_for_wiki(keywords)
        print(f"🔍 Searching Wikipedia for: '{cleaned_keywords}'")
        
        results = self.search(cleaned_keywords)
        
        if not results:
            print("No results found!")
            return []
        
        scraped_articles = []
        
        for i, (title, url) in enumerate(results[:max_articles], 1):
            print(f"[{i}/{min(max_articles, len(results))}] Scraping: {title}")
            
            result = self.scrape_article(url)
            if result:
                article_title, content = result
                scraped_articles.append({
                    'title': article_title,
                    'content': content,
                    'url': url
                })
                print(f"   ✓ Scraped successfully")
            else:
                print(f"   ✗ Failed to scrape article")
            
            # Be nice to Wikipedia servers
            time.sleep(1)
        
        print(f"✅ Successfully scraped {len(scraped_articles)} Wikipedia articles!")
        return scraped_articles
