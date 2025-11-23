# tools.py
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# === Search tool (DuckDuckGo) ===
search_runner = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search_runner.run,
    description="Search the web for information. Input: a query string. Output: search results text."
)

# === Wikipedia tool (wrapper) ===
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_runner = WikipediaQueryRun(api_wrapper=api_wrapper)
wiki_tool = Tool(
    name="Wikipedia",
    func=wiki_runner.run,
    description="Query Wikipedia for a topic. Input: a wiki query string. Output: article text."
)

# === Save tool ===
def save_to_txt(data: str, filename: str = "Research_Output.txt"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_to_txt",
    func=save_to_txt,
    description="Save the given text to a txt file. Input: text string."
)
