import requests
from bs4 import BeautifulSoup
from datetime import date

def get_article_content(url):
    """Visits the article to check for AI keywords in the body text."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content_text = " ".join([p.get_text() for p in paragraphs[:5]])
        return content_text.lower()
    except:
        return ""

def get_filtered_news():
    categories = ['technology', 'business']
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'openai', 'robot', 'llm', 'gpu']
    
    final_ai_news = [] # This will now store dictionaries
    headers = {'User-Agent': 'Mozilla/5.0'}

    for cat in categories:
        url = f"https://www.bbc.com/news/{cat}"
        print(f"Searching {cat} for AI stories...")
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                title = link.get_text().strip()
                path = link['href']
                
                if "/news/" in path and len(title) > 30:
                    full_url = f"https://www.bbc.com{path}" if path.startswith('/') else path
                    
                    # Logic to check if it's AI news
                    content = get_article_content(full_url)
                    is_ai = any(word in title.lower() for word in ai_keywords) or \
                            any(word in content for word in ai_keywords)
                    
                    if is_ai:
                        # STORE: Header, Link, and Date
                        news_data = {
                            "header": title,
                            "link": full_url,
                            "date": date.today().strftime("%Y-%m-%d")
                        }
                        # Avoid duplicates
                        if news_data not in final_ai_news:
                            final_ai_news.append(news_data)
        except Exception as e:
            print(f"Error: {e}")

    return final_ai_news