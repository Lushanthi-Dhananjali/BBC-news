from langchain_ollama import ChatOllama
from scraper import get_weekly_report  # This imports your Step 2 code

# 1. Setup your Local LLM (No API Key needed)
llm = ChatOllama(
    model="llama3",
    temperature=0.2, # Low temperature for factual news summaries
)

def run_news_agent():
    print("Agent: I am fetching the latest Tech and Business news for you...")
    
    # 2. Get the raw news using your scraper tool
    raw_news = get_weekly_report()
    
    # 3. Create the instruction for Llama 3
    prompt = f"""
    You are a professional News Assistant. 
    Below is a list of news headlines from the BBC. 
    Please provide a 3-sentence summary of the most important trends for a Computer Engineer.
    
    NEWS DATA:
    {raw_news}
    """
    
    # 4. Ask Llama 3 to summarize
    response = llm.invoke(prompt)
    
    print("\n--- YOUR WEEKLY BRIEFING ---")
    print(response.content)

if __name__ == "__main__":
    run_news_agent()