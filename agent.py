import csv
from scraper import get_filtered_ai_news
from langchain_ollama import ChatOllama # Ensure you have this installed

# Setup Llama 3
llm = ChatOllama(model="llama3", temperature=0.1)

def start_step_4():
    print("=== Step 4: Summarizing & Storing AI News ===")
    
    # Steps 1-3 happen inside this call
    ai_news_list = get_filtered_ai_news()
    
    if not ai_news_list:
        print("\nNo genuine AI news found.")
        return

    # CSV setup
    filename = "Verified_AI_News_Report.csv"
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Header", "Publish Date", "Link", "Summary"])

        for item in ai_news_list:
            print(f"Summarizing: {item['header'][:50]}...")
            
            # Use Llama 3 to create a small summary
            prompt = f"Summarize this AI news technically in 2 sentences: {item['content']}"
            try:
                summary = llm.invoke(prompt).content.strip()
            except:
                summary = "Summary failed."

            writer.writerow([item['header'], item['date'], item['link'], summary])

    print(f"\n✅ SUCCESS! File created: {filename}")

if __name__ == "__main__":
    start_step_4()