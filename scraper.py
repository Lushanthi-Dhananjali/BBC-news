import requests
from bs4 import BeautifulSoup

def get_article_content(url):
    """Visits the actual article page to check for AI keywords in the body text."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BBC article text is usually inside <p> tags
        paragraphs = soup.find_all('p')
        # We only read the first 5 paragraphs to stay fast
        content_text = " ".join([p.get_text() for p in paragraphs[:5]])
        return content_text.lower()
    except:
        return ""

def get_filtered_news():
    categories = ['technology', 'business']
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'openai', 'robot', 'llm', 'gpu']
    
    final_ai_news = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for cat in categories:
        url = f"https://www.bbc.com/news/{cat}"
        print(f"Searching {cat} for AI stories...")
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links that look like news articles
        links = soup.find_all('a', href=True)
        
        for link in links:
            title = link.get_text().strip()
            path = link['href']
            
            # Ensure it's a real news link and not a menu item
            if "/news/" in path and len(title) > 30:
                full_url = f"https://www.bbc.com{path}" if path.startswith('/') else path
                
                # Check Headline FIRST
                if any(word in title.lower() for word in ai_keywords):
                    final_ai_news.append(f"TITLE MATCH: {title}")
                    continue # Skip content check if headline already matched
                
                # Check CONTENT SECOND (If headline didn't match)
                content = get_article_content(full_url)
                if any(word in content for word in ai_keywords):
                    final_ai_news.append(f"CONTENT MATCH: {title}")

    # Remove duplicates
    return list(dict.fromkeys(final_ai_news))

if __name__ == "__main__":
    results = get_filtered_news()
    for item in results:
        print(f"Found: {item}")