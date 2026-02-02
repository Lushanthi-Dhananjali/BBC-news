import requests
from bs4 import BeautifulSoup

def get_bbc_headers():
    url = "https://www.bbc.com/news"
    
    # 1. Send request to BBC
    print(f"Connecting to {url}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        # 2. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Find all <h3> tags (common for BBC headlines)
        headlines = soup.find_all('h3')
        
        # 4. Clean and filter the results
        clean_headlines = [h.get_text().strip() for h in headlines if h.get_text()]
        
        # Remove duplicates
        unique_headlines = list(dict.fromkeys(clean_headlines))
        
        return unique_headlines
    else:
        return f"Failed to connect. Status code: {response.status_code}"

# Testing Step 1
if __name__ == "__main__":
    headers = get_bbc_headers()
    print("\n--- BBC News Headers ---")
    for i, title in enumerate(headers[:10], 1):  # Display top 10
        print(f"{i}. {title}")