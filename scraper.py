import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_bbc_category_news(category):
    """
    Scrapes headers from specific BBC categories.
    Valid categories: 'technology', 'business'
    """
    url = f"https://www.bbc.com/news/{category}"
    print(f"Fetching {category.upper()} news...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BBC uses <h2> or <h3> for news headlines depending on the layout
        headlines = soup.find_all(['h2', 'h3'])
        
        # Clean and filter unique headers
        results = []
        for h in headlines:
            text = h.get_text().strip()
            # Filter out short menu items or button text (usually < 15 chars)
            if len(text) > 20 and text not in results:
                results.append(text)
        
        return results
    except Exception as e:
        return [f"Error: {e}"]

# --- Main Execution ---
if __name__ == "__main__":
    # Categories requested
    categories = ['technology', 'business']
    
    weekly_news_report = {}

    for cat in categories:
        titles = get_bbc_category_news(cat)
        # We take the top 5-10 to keep it relevant to 'this week'
        weekly_news_report[cat] = titles[:8] 

    # Print the Results
    print("\n" + "="*30)
    print("WEEKLY NEWS FILTER")
    print("="*30)
    for cat, news in weekly_news_report.items():
        print(f"\n[{cat.upper()}]")
        for i, title in enumerate(news, 1):
            print(f"{i}. {title}")