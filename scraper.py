import requests
from bs4 import BeautifulSoup
from datetime import date

def get_article_content(url):
    """Fetches article text but returns only the first 2000 chars to save memory."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        # We only grab enough text for a good summary, not the whole database
        content_text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text()) > 40])
        return content_text[:3000] # Limit to 3000 chars for the LLM
    except:
        return ""

def get_filtered_news():
    categories = ['technology', 'business']
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'openai', 'robot', 'llm', 'gpu']
    
    final_ai_news = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for cat in categories:
        url = f"https://www.bbc.com/news/{cat}"
        print(f"Scanning {cat.upper()}...")
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for link in links:
            title = link.get_text().strip()
            path = link['href']
            
            if "/news/" in path and len(title) > 30:
                full_url = f"https://www.bbc.com{path}" if path.startswith('/') else path
                content = get_article_content(full_url)
                
                # Filter check
                if any(word in title.lower() for word in ai_keywords) or any(word in content.lower() for word in ai_keywords):
                    news_data = {
                        "header": title,
                        "link": full_url,
                        "date": date.today().strftime("%Y-%m-%d"),
                        "raw_text": content # Temporary storage for the agent to summarize
                    }
                    if not any(d['header'] == title for d in final_ai_news):
                        final_ai_news.append(news_data)
    return final_ai_news