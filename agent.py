import csv
from langchain_ollama import ChatOllama
from scraper import get_bbc_news_by_category
from datetime import date

# 1. Setup Local LLM
llm = ChatOllama(model="llama3", temperature=0.1)

def run_project():
    # Step 2: Fetch raw headers
    print("Fetching news from BBC...")
    raw_tech = get_bbc_news_by_category("technology")
    raw_biz = get_bbc_news_by_category("business")
    all_raw_news = raw_tech + raw_biz

    # Step 3: AI Keyword Filter (Headers only)
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'openai', 'chatgpt', 'robot', 'gpu', 'nvidia']
    
    # Filter the list
    filtered_news = []
    for item in all_raw_news:
        header = item['header'].lower()
        if any(keyword in header for keyword in ai_keywords):
            filtered_news.append(item)

    if not filtered_news:
        print("No AI news found in today's headers.")
        return

    # Step 4: Summarize and Store
    print(f"Filtering complete. Found {len(filtered_news)} AI stories. Summarizing...")
    filename = f"AI_News_{date.today()}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Header", "Date", "Link", "Summary"])

        for item in filtered_news:
            h = item['header']
            print(f"Processing: {h[:50]}...")
            
            # Generate summary with Llama 3
            prompt = f"Summarize this news headline in one short technical sentence: {h}"
            try:
                summary = llm.invoke(prompt).content.strip()
            except:
                summary = "Summary generation failed."

            # Save Row
            writer.writerow([h, item['date'], item['link'], summary])

    print(f"\n✅ SUCCESS! Your report is ready: {filename}")

if __name__ == "__main__":
    run_project()