import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional, Any
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
import re
import json
import difflib

# Configure logging
logger = logging.getLogger(__name__)

class ScraperService:
    BASE_URL = "https://www.himolde.no"
    PROGRAMS_URL = f"{BASE_URL}/studier/programmer/"
    USER_AGENT = "ibe160-chatbot-student-project/0.1"
    
    # Sections to crawl
    SECTIONS_TO_CRAWL = [
        "https://www.himolde.no/studier/programmer/",
        "https://www.himolde.no/studier/opptak/",
        "https://www.himolde.no/studentliv/",
        "https://www.himolde.no/om/"
    ]

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})
        
        self.course_map = {}
        self.course_db = {"codes": {}, "names": {}}
        try:
            # Load course link map if available
            db_path = Path("backend/data/course_database.json")
            if db_path.exists():
                with open(db_path, "r", encoding="utf-8") as f:
                    self.course_db = json.load(f)
                logger.info(f"Loaded {len(self.course_db['codes'])} codes and {len(self.course_db['names'])} names from DB.")
        except Exception as e:
            logger.warning(f"Failed to load course DB: {e}")

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

    def scrape_everything(self) -> List[Dict[str, Any]]:
        """Scrape multiple sections of the website."""
        all_documents = []
        
        for section_url in self.SECTIONS_TO_CRAWL:
            logger.info(f"Starting crawl of section: {section_url}")
            docs = self._crawl_section(section_url)
            all_documents.extend(docs)
            
        return all_documents

    def _crawl_section(self, section_url: str) -> List[Dict[str, Any]]:
        """Crawl a specific section finding relevant pages."""
        try:
            response = self._fetch(section_url)
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        documents = []
        seen_urls = set()

        # Gather links that belong to this section
        import urllib.parse
        parsed_section = urllib.parse.urlparse(section_url)
        section_path = parsed_section.path

        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)
            
            full_url = self._normalize_url(href)
            
            # Filter: Check if it belongs to the section 
            if section_path in full_url and self._is_valid_content_url(full_url):
                 if full_url not in seen_urls:
                    seen_urls.add(full_url)
                    logger.info(f"Found page: {text} -> {full_url}")
                    
                    details_list = self.scrape_page_details(full_url)
                    if details_list:
                        # Ensure title exists on the main doc if missing
                        if not details_list[0].get("title"):
                            details_list[0]["title"] = text
                        documents.extend(details_list)
        
        return documents

    def scrape_url(self, url: str) -> List[Dict[str, Any]]:
        """Scrape a single URL (public interface)."""
        logger.info(f"Directly scraping URL: {url}")
        return self.scrape_page_details(url)

    def scrape_page_details(self, url: str) -> List[Dict[str, Any]]:
        """Deep scrape a specific page, including sub-pages and courses if applicable."""
        try:
            response = self._fetch(url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract basic metadata
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Page"
            
            # Extract Brief Description
            intro = ""
            intro_tag = soup.find(class_="lead") or soup.find("p", class_="intro")
            if intro_tag:
                 intro = intro_tag.get_text(strip=True)

            content_blocks = []
            
            # 1. Main Content
            main_content = soup.find("article") or soup.find("main") or soup.find("div", id="main-content")
            if main_content:
                # Remove tabs content that we scrape separately (Structure, Learning)
                # This prevents "Duplicate Content" that is poorly formatted in the main chunk.
                for hidden in main_content.find_all(class_=["term", "study-plan", "course-list"]):
                    hidden.decompose()
                
                self._clean_soup(main_content)
                self._inject_markdown_links(main_content)
                content_blocks.append(main_content.get_text(separator="\n", strip=True))

            # 2. Check for Sub-Pages (Structure, Learning, Career) for Programs
            additional_docs = []
            if "/studier/programmer/" in url:
                sub_links_sigs = [
                    ("Hva lærer du?", "LEARNING OUTCOMES"), 
                    ("Oppbygging og gjennomføring", "STRUCTURE"),
                    ("Jobbmuligheter", "CAREER")
                ]
                
                for text_sig, header_sig in sub_links_sigs:
                    link = soup.find("a", string=lambda t: t and text_sig.lower() in t.lower())
                    if link and link.get("href"):
                         sub_url = self._normalize_url(link["href"])
                         try:
                             # Fetch sub-page
                             sub_resp = self._fetch(sub_url)
                             sub_soup = BeautifulSoup(sub_resp.content, "html.parser")
                             sub_main = sub_soup.find("article") or sub_soup.find("main")
                             
                             if sub_main:
                                 # Special Handling for STRUCTURE page
                                 if header_sig == "STRUCTURE":
                                      # 1. Scrape courses as separate docs
                                      course_docs = self._scrape_courses_from_structure(sub_soup)
                                      additional_docs.extend(course_docs)
                                      
                                      # 2. Extract Course Links for deterministic list generation
                                      # Instead of relying on get_text(), we build a clean Markdown list
                                      course_list_md = ["## Emner og Fagliste (Courses)"]
                                      found_courses = set()
                                      
                                      # 1. Capture Linked Courses
                                      for a in sub_main.find_all("a", href=True):
                                          href = a["href"]
                                          if "/studier/emner/" in href or "/english/studies/courses/" in href:
                                              full_link = self._normalize_url(href)
                                              name = a.get_text(strip=True)
                                              course_list_md.append(f"* [{name}]({full_link})")
                                              # Extract code like IBE102 from "IBE102 Webutvikling" for de-duplication
                                              code_match = re.search(r'([A-Z]{3}\d{3})', name)
                                              if code_match:
                                                  found_courses.add(code_match.group(1))
                                      
                                      # 0. Try Structured Parsing (User Strategy)
                                      structure_content = self._parse_study_model(sub_main)
                                      
                                      if structure_content:
                                          structure_doc = {
                                              "url": sub_url,
                                              # Append semantic keywords to ensure all chunks (including Spring/2nd page) are retrieved for "courses"/"fag" queries
                                              "title": f"{title} - Oppbygging og gjennomføring - Fagliste (Course List)",
                                              "content": structure_content,
                                              "metadata": {"type": "subpage", "parent_title": title},
                                              "source": "himolde.no"
                                          }
                                          additional_docs.append(structure_doc)
                                          sub_text = "" # Clear sub_text as content is now in a separate doc
                                      else:
                                          # Fallback: Raw text with header link prepending
                                          self._clean_soup(sub_main)
                                          sub_text = sub_main.get_text(separator='\n', strip=True)

                                          if course_list_md:
                                               course_list_block = "\n".join(course_list_md)
                                               sub_text = f"{course_list_block}\n\n{sub_text}"
                                 else:
                                     self._clean_soup(sub_main)
                                     sub_text = sub_main.get_text(separator='\n', strip=True)
                                 
                                 # Create separate document for this sub-page
                                 sub_doc = {
                                     "title": f"{title} - {text_sig}",
                                     "url": sub_url,
                                     "description": f"{text_sig} section for {title}",
                                     "content": sub_text,
                                     "metadata": {"type": "subpage", "parent_title": title},
                                     "source": "himolde.no"
                                 }
                                 additional_docs.append(sub_doc)

                         except Exception as e:
                             logger.warning(f"Could not fetch sub-page {header_sig} for {url}: {e}")

            # Main Doc (Landing Page only now)
            full_content = "\n\n".join(content_blocks)

            main_doc = {
                "title": title,
                "url": url,
                "description": intro,
                "content": full_content,
                "source": "himolde.no"
            }
            
            return [main_doc] + additional_docs

        except Exception as e:
            logger.error(f"Failed to scrape details for {url}: {e}")
            return None

    def _parse_study_model(self, soup) -> str:
        """
        Parses the 'Studiemodell' HTML structure into a Markdown table.
        Returns empty string if structure not found.
        """
        md_output = []
        md_output = []
        # Use H1 and verbose description to boost embedding relevance for "courses" queries
        md_output.append("# Studiemodell og Fagplan (Structure and Course List)")
        md_output.append("FAQ: Hvilke fag inngår i Årsstudium i logistikk? Hva slags emner lærer man? (What courses are included?)")
        md_output.append("Svar: Dette er den offisielle oversikten over alle fag og emner som inngår i studiet:")
        
        terms = soup.find_all("div", class_="term")
        if not terms:
            return ""

        for term in terms:
            header = term.find("h3")
            semester_name = header.get_text(strip=True) if header else "Semester"
            md_output.append(f"\n### {semester_name}")
            
            # Create Table Header
            md_output.append("| Code | Course Name | Credits |")
            md_output.append("| :--- | :--- | :--- |")
            
            course_list = term.find("ul", class_="course-list")
            if not course_list:
                continue
                
            items = course_list.find_all("li")
            for item in items:
                link = item.find("a", class_="course-link")
                if not link:
                    continue
                    
                href = self._normalize_url(link["href"])
                
                code_span = link.find("span", class_="course-code")
                code = code_span.get_text(strip=True) if code_span else "N/A"
                
                name_span = link.find("span", class_="course-name")
                name = name_span.get_text(strip=True) if name_span else "Unknown Course"
                
                points_span = link.find("span", class_="course-study-points")
                points = points_span.get_text(" ", strip=True) if points_span else ""
                
                # Format row
                # Link both code and name for maximum clickability
                row = f"| [{code}]({href}) | [{name}]({href}) | {points} |"
                md_output.append(row)
                
        return "\n".join(md_output)

    def _scrape_courses_from_structure(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Find course links in structure page and scrape them as separate documents."""
        # Find all links containing /studier/emner/
        course_links = soup.find_all("a", href=lambda h: h and "/studier/emner/" in h)
        
        seen_courses = set()
        course_docs = []
        
        for link in course_links:
            course_url = self._normalize_url(link["href"])
            if course_url in seen_courses:
                continue
            seen_courses.add(course_url)
            
            try:
                # Fetch Course Page
                resp = self._fetch(course_url)
                c_soup = BeautifulSoup(resp.content, "html.parser")
                
                c_title = c_soup.find("h1").get_text(strip=True) if c_soup.find("h1") else "Unknown Course"
                c_main = c_soup.find("article") or c_soup.find("main")
                
                if c_main:
                    self._clean_soup(c_main)
                    c_text = c_main.get_text(separator="\n", strip=True)
                    
                    course_doc = {
                        "title": c_title,
                        "url": course_url,
                        "description": f"Course description for {c_title}",
                        "content": c_text,
                        "source": "himolde.no"
                    }
                    course_docs.append(course_doc)
                    logger.info(f"Scraped course: {c_title}")
                    
            except Exception as e:
                 logger.warning(f"Failed to scrape course {course_url}: {e}")
                 
        return course_docs

    def _normalize_url(self, href: str) -> str:
        if href.startswith("/"):
            return f"{self.BASE_URL}{href}"
        if not href.startswith("http"):
             return f"{self.BASE_URL}/{href}"
        return href

    def _is_valid_content_url(self, url: str) -> bool:
        """Filter to valid content URLs."""
        if "?" in url or "#" in url:
            return False
        
        invalid_exts = ['.pdf', '.jpg', '.png', '.doc', '.docx', '.zip']
        if any(url.endswith(ext) for ext in invalid_exts):
            return False
            
        return True

    def _clean_soup(self, soup: Tag):
        """Remove unwanted tags in-place."""
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

    def _inject_markdown_links(self, soup: Tag):
        """
        Replaces <a> tags with their Markdown equivalent [Text](URL) in-place.
        This ensures links are preserved in the RAG chunks.
        """
        for a in soup.find_all("a", href=True):
            href = self._normalize_url(a["href"])
            text = a.get_text(strip=True)
            if text and href and "himolde.no" in href: # Only link internal/valid content
                 if not text.startswith("["): # Avoid double linking if already processed
                    new_text = f"[{text}]({href})"
                    a.replace_with(new_text)
