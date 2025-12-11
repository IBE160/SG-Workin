import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ScraperService:
    BASE_URL = "https://www.himolde.no"
    PROGRAMS_URL = f"{BASE_URL}/studier/programmer/"
    USER_AGENT = "ibe160-chatbot-student-project/0.1"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    @retry(
        retry=retry_if_exception_type(requests.RequestException),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch(self, url: str) -> requests.Response:
        """Robustly fetch a URL with retries."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

    def scrape_all_programs(self) -> List[Dict[str, Any]]:
        """Main entry point: Scrape all programs and their details."""
        logger.info(f"Starting crawl of {self.PROGRAMS_URL}")
        
        # 1. Fetch Listing
        try:
            response = self._fetch(self.PROGRAMS_URL)
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        
        # 2. Extract Program Links
        # Targeting the list items. Based on typical structure, usually inside a generic container.
        # We'll look for links containing '/studier/programmer/' but distinct from the base.
        # Probing showed <a href="..."> inside headers or lists.
        # A specific selector might be safer, but broad search is more resilient for now.
        
        programs = []
        # Finding all links that look like program detail pages
        # Probing confirmed URls like: /studier/programmer/it-og-digitalisering/index.html
        
        seen_urls = set()
        
        # Heuristic: Find links in the main content area
        # Assuming there is a main container, but 'body' search with filtering is robust enough for headers.
        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)
            
            if not href.startswith("http"):
                # Handle relative links
                 href = self._normalize_url(href)

            # Filter relevant program URLs
            if self._is_program_url(href) and href not in seen_urls:
                seen_urls.add(href)
                logger.info(f"Found program: {text} -> {href}")
                
                # 3. Deep Scrape (Detail Page)
                details = self.scrape_program_details(href)
                if details:
                    # Merge basic info if missing, though detail scrape should cover it
                    if not details.get("title"):
                        details["title"] = text
                    
                    programs.append(details)
        
        return programs

    def scrape_program_details(self, url: str) -> Optional[Dict[str, Any]]:
        """Deep scrape a specific program page."""
        try:
            response = self._fetch(url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract basic metadata
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Program"
            
            # Extract Brief Description (usually lead paragraph)
            intro = ""
            intro_tag = soup.find(class_="lead") or soup.find("p", class_="intro")
            if intro_tag:
                 intro = intro_tag.get_text(strip=True)

            # Extract Deep Content Sections
            # We look for sections like "Fakta", "Hva lærer du", etc.
            # Strategy: Grab all text for now, but formatted nicely.
            
            content_blocks = []
            
            # 1. Main Content of Index Page
            # We assume unique ID or typical article tag
            main_content = soup.find("article") or soup.find("main") or soup.find("div", id="main-content")
            if main_content:
                # Remove navigation, scripts, etc. derived from generic cleaning
                self._clean_soup(main_content)
                content_blocks.append(main_content.get_text(separator="\n", strip=True))

            # 2. Follow "Hva lærer du?" / "Oppbygging" sub-links if they exist
            # Note: This increases traffic significantly. For MVP we might skip recursive sub-crawling 
            # if the index page contains summary tabs. 
            # PROBING REVEALED: "Studenters erfaringer", "Oppbygging og gjennomføring" are links.
            # Let's try to fetch at least "Hva lærer du" if present linked.
            
            learning_link = soup.find("a", string=lambda t: t and "lærer du" in t.lower())
            if learning_link and learning_link.get("href"):
                 learning_url = self._normalize_url(learning_link["href"])
                 try:
                     l_resp = self._fetch(learning_url)
                     l_soup = BeautifulSoup(l_resp.content, "html.parser")
                     l_main = l_soup.find("article") or l_soup.find("main")
                     if l_main:
                         self._clean_soup(l_main)
                         content_blocks.append(f"\n--- LEARNING OUTCOMES ---\n{l_main.get_text(separator='\n', strip=True)}")
                 except Exception as e:
                     logger.warning(f"Could not fetch learning outcomes for {title}: {e}")

            full_content = "\n\n".join(content_blocks)

            return {
                "title": title,
                "url": url,
                "description": intro,
                "content": full_content, # Deep content
                "source": "himolde.no"
            }

        except Exception as e:
            logger.error(f"Failed to scrape details for {url}: {e}")
            return None

    def _normalize_url(self, href: str) -> str:
        if href.startswith("/"):
            return f"{self.BASE_URL}{href}"
        return href

    def _is_program_url(self, url: str) -> bool:
        """Filter to valid program URLs."""
        # Must be in /studier/programmer/
        if "/studier/programmer/" not in url:
            return False
        # Ignore the main listing page itself
        if url.endswith("/studier/programmer/") or url.endswith("/studier/programmer/index.html"):
            return False
        # Ignore random assets or query params
        if "?" in url or "#" in url:
            return False
            
        return True

    def _clean_soup(self, soup: Tag):
        """Remove unwanted tags in-place."""
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
