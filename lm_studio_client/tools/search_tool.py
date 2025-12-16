import sys
import os
import requests
import concurrent.futures
from bs4 import BeautifulSoup

# Add parent directory to path to import BaseTool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from base_tool import BaseTool
    from googlesearch import search
except ImportError as e:
    if "googlesearch" in str(e):
        print("Error: 'googlesearch-python' library is missing.")
    from lm_studio_client.base_tool import BaseTool

class SearchTool(BaseTool):
    @property
    def name(self):
        return "internet_search"

    @property
    def description(self):
        return "Useful for finding information on the internet. Searches Google, opens the top 10 results, and returns their text content combined."

    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search keywords or question to look up."
                }
            },
            "required": ["query"]
        }

    def _scrape_url(self, url):
        """
        Helper function to scrape a single URL.
        """
        try:
            # mimic a browser to avoid being blocked by some sites
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements to clean up text
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Get text and clean up whitespace
            text = soup.get_text(separator=' ', strip=True)
            
            # Truncate very long pages to prevent context window overflow (e.g., first 1000 chars)
            # You can adjust this limit based on your LLM's context size.
            preview_text = text[:1500] + "..." if len(text) > 1500 else text

            return f"--- Source: {url} ---\n{preview_text}\n"

        except Exception as e:
            return f"--- Source: {url} ---\nError: Could not scrape content ({str(e)})\n"

    def execute(self, query):
        """
        Executes the Google search and scrapes results concurrently.
        """
        try:
            print(f"Searching for: {query}...")
            urls = []
            # Get top 10 URLs
            for url in search(query, num=10, stop=10, pause=2.0):
                urls.append(url)
            
            if not urls:
                return "No search results found."

            print(f"Found {len(urls)} links. Scraping content...")
            
            results = []
            # Use ThreadPoolExecutor to scrape URLs in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Submit all scraping tasks
                future_to_url = {executor.submit(self._scrape_url, url): url for url in urls}
                
                # Gather results as they complete
                for future in concurrent.futures.as_completed(future_to_url):
                    results.append(future.result())

            # Combine all results into one mega string
            final_output = "\n".join(results)
            return final_output

        except Exception as e:
            return f"Error performing search and scrape: {str(e)}"