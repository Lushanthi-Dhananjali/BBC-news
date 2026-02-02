import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_bbc_news_by_category(category):
    """
    Step 1 & 2: Go to BBC and get headers from Technology/Business.
    """
    url = f"https://www.bbc.com/news/{category}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    news_list = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BBC headlines are usually in h2 or h3 tags
        articles = soup.find_all(['h2', 'h3'])
        
        for article in articles:
            title = article.get_text().strip()
            # Find the link associated with this header
            parent_a = article.find_parent('a') or article.find('a')
            
            if parent_a and parent_a.has_attr('href'):
                link = parent_a['href']
                full_url = f"https://www.bbc.com{link}" if link.startswith('/') else link
                
                # Basic validation: ensure it's a real news story
                if "/news/" in full_url and len(title) > 25:
                    news_list.append({
                        "header": title,
                        "link": full_url,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
        return news_list
    except Exception as e:
        print(f"Error fetching {category}: {e}")
        return []