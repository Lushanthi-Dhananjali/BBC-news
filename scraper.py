import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def get_filtered_ai_news():
    categories = ['technology', 'health']
    # Match 'AI' as a whole word or the full phrases
    ai_pattern = re.compile(r'\b(ai|artificial intelligence|machine learning|chatgpt|openai|llm)\b', re.IGNORECASE)
    
    # Negative filter: If these words are found, discard the article
    blacklist = ['parking', 'parking fine', 'solar panel', 'weight loss', 'strike action', 'pension']
    
    verified_ai_news = []
    one_week_ago = datetime.now() - timedelta(days=7)
    headers = {'User-Agent': 'Mozilla/5.0'}

    for cat in categories:
        url = f"https://www.bbc.com/news/{cat}"
        print(f"Scanning BBC {cat.upper()} for REAL AI stories...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                path = link['href']
                full_url = f"https://www.bbc.com{path}" if path.startswith('/') else path
                
                if "/news/articles/" in path or "/news/videos/" in path:
                    try:
                        article_res = requests.get(full_url, headers=headers, timeout=5)
                        article_soup = BeautifulSoup(article_res.text, 'html.parser')
                        
                        # Step 1: Date Check
                        time_tag = article_soup.find('time')
                        if time_tag and time_tag.has_attr('datetime'):
                            date_str = time_tag['datetime'][:10] 
                            pub_date = datetime.strptime(date_str, '%Y-%m-%d')
                            
                            if pub_date >= one_week_ago:
                                # Step 2: Content Check
                                paragraphs = article_soup.find_all('p')
                                content_text = " ".join([p.get_text() for p in paragraphs]).lower()
                                
                                # Strict Regex Match
                                if ai_pattern.search(content_text):
                                    # Strict Blacklist Check
                                    if not any(bad_word in content_text for bad_word in blacklist):
                                        header_tag = article_soup.find('h1')
                                        if header_tag:
                                            title = header_tag.get_text().strip()
                                            if not any(item['header'] == title for item in verified_ai_news):
                                                verified_ai_news.append({
                                                    "header": title,
                                                    "link": full_url,
                                                    "date": date_str,
                                                    "content": content_text[:2000] # For LLM
                                                })
                                                print(f"  [Verified AI]: {title[:50]}...")
                    except:
                        continue
        except Exception as e:
            print(f"Error: {e}")

    return verified_ai_news