from typing import List
import re
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_core.documents import Document

def extract_clean_text(html: str) -> str:
    """
    Parses HTML and extracts clean text from the main article section,
    stripping out navbars, headers, footers, and code-copy buttons.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    main_content = soup.find("main") or soup.find("article") or soup.body
    
    if main_content:
        for element in main_content(["script", "style", "nav", "footer"]):
            element.decompose()
        return main_content.get_text(separator="\n", strip=True)
    
    return ""

def scrape_angular_docs(
    root_url: str = "https://angular.dev/guide/",
    max_depth: int = 3,
    max_pages: int = 100
) -> List[Document]:
    """
    Recursively crawls angular.dev documentation routes starting from the root URL.
    """
    print(f"Starting recursive crawl at: {root_url} (Max Depth: {max_depth})")
    
    loader = RecursiveUrlLoader(
        url=root_url,
        max_depth=max_depth,
        extractor=extract_clean_text,
        prevent_outside=True,  
        use_async=True,     
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    
    documents = loader.load()
    
    print(f"Crawling finished! Successfully collected {len(documents)} document pages.")
    return documents



# Another possible way

# from typing import List
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_core.documents import Document

# # Key entry URLs from Angular documentation to scrape
# ANGULAR_DOC_URLS = [
#     "https://angular.dev/overview",
#     "https://angular.dev/guide/signals",
#     "https://angular.dev/guide/components",
#     "https://angular.dev/guide/templates/control-flow",
#     "https://angular.dev/guide/di",
#     "https://angular.dev/guide/di/defining-dependency-providers",
#     "https://angular.dev/guide/di/dependency-injection-context",
#     "https://angular.dev/guide/di/creating-and-using-services",
#     "https://angular.dev/guide/di/lazy-loading-services",
#     "https://angular.dev/guide/di/hierarchical-dependency-injection",
#     "https://angular.dev/guide/routing",
#     "https://angular.dev/guide/forms",
#     "https://angular.dev/guide/http",
# ]

# def load_documents_from_web(urls: List[str] = ANGULAR_DOC_URLS) -> List[Document]:
#     """
#     Scrapes HTML content directly from the provided Angular documentation URLs
#     and converts them into LangChain Document objects.
#     """
    
#     loader = WebBaseLoader(
#         web_paths=urls,
#         # Set a standard User-Agent header so request isn't blocked by basic bot detection
#         header_template={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
#         }
#     )
    
#     # Optional: Filter out unnecessary HTML elements (navbars, footers, scripts)
#     loader.requests_per_second = 2
#     docs = loader.load()
    
#     print(f"Successfully scraped {len(docs)} pages.")
#     return docs


