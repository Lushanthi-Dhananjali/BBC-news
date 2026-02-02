import csv
from langchain_ollama import ChatOllama
from scraper import get_filtered_news  # Your Step 3 logic
from datetime import date

# 1. Setup Local Llama 3
llm = ChatOllama(model="llama3", temperature=0.1)

def save_and_summarize():
    # 2. Get the AI News (Header and Link)
    print("Searching for AI news...")
    news_items = get_filtered_news() 
    
    if not news_items:
        print("No AI news found today.")
        return

    # 3. Create a CSV file to store data
    filename = f"AI_News_{date.today()}.csv"
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Header", "Summary"]) # CSV Columns

        print(f"\nProcessing {len(news_items)} stories...")
        
        for item in news_items:
            # We assume the scraper returns "Title: [URL]" or similar
            # If your scraper returns a list of strings, adjust here
            header = item
            
            # 4. Ask Llama 3 to summarize the header/context
            prompt = f"Provide a 1-sentence technical summary of this news for a Computer Engineer: {header}"
            summary = llm.invoke(prompt).content
            
            # 5. Save to CSV
            writer.writerow([date.today(), header, summary])
            print(f"Stored: {header[:50]}...")

    print(f"\nSuccess! Your AI News Report is saved in: {filename}")

if __name__ == "__main__":
    save_and_summarize()