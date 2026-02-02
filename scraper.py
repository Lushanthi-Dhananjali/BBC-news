import requests
from bs4 import BeautifulSoup

def get_filtered_news():
    # 1. Define the categories and AI keywords
    categories = ['technology', 'business']
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'openai', 'robot', 'automation']
    
    all_news = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Fetching news from BBC...")

    for category in categories:
        url = f"https://www.bbc.com/news/{category}"
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find headlines (usually h2 or h3)
            headlines = soup.find_all(['h2', 'h3'])
            
            for h in headlines:
                text = h.get_text().strip()
                
                # Filter 1: Only keep long headlines (removes menu buttons)
                if len(text) > 25:
                    # Filter 2: Check if any AI keyword is in the headline
                    is_ai_related = any(word in text.lower() for word in ai_keywords)
                    
                    if is_ai_related:
                        if text not in all_news: # Remove duplicates
                            all_news.append(f"[{category.upper()}] {text}")
                            
        except Exception as e:
            print(f"Error fetching {category}: {e}")

    return all_news

# This part is just for testing!
if __name__ == "__main__":
    ai_stories = get_filtered_news()
    print("\n--- FOUND AI RELATED NEWS ---")
    if not ai_stories:
        print("No AI news found today. Try again later!")
    else:
        for i, news in enumerate(ai_stories, 1):
            print(f"{i}. {news}")