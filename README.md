# 🤖 AI Search Agent

**Intelligent Research Assistant with Multi-Tool Integration**

An advanced AI-powered search and research agent that leverages multiple tools including web search, Wikipedia lookup, and file operations to provide comprehensive research capabilities with automatic output saving and structured responses.

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.0-1c3c3c?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.11+-e92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://pydantic.dev/)

## 🌟 Features

- 🧠 **Intelligent Research** - Multi-source research using web search and Wikipedia
- 🔍 **Web Search Integration** - Real-time web search via DuckDuckGo
- 📚 **Wikipedia Integration** - Comprehensive encyclopedia lookup
- 💾 **Auto-Save Results** - Automatic research output saving to text files
- 🤖 **Tool-Calling Agent** - Advanced LangChain agent with structured outputs
- 📊 **Structured Responses** - Pydantic-based response formatting with validation
- ⚡ **OpenAI GPT-4o** - Powered by the latest OpenAI language model
- 🕒 **Timestamped Outputs** - Automatic timestamp tracking for research sessions

## 🛠️ Tech Stack

**Backend:** Python 3.8+, LangChain, OpenAI GPT-4o  
**Search Tools:** DuckDuckGo Search, Wikipedia API  
**Data Processing:** Pydantic for structured outputs and validation  
**File Operations:** Automated text file generation with timestamps  
**Agent Framework:** LangChain tool-calling agent architecture

## 🏗️ Agent Architecture

The system uses a sophisticated tool-calling agent architecture built with LangChain:

### Core Components

- **🤖 LangChain Agent** - Tool-calling agent with GPT-4o integration
- **🔍 Search Tools** - Web search and Wikipedia lookup capabilities
- **💾 File Operations** - Automated research output saving with timestamps
- **� Structured Output** - Pydantic models for consistent response formatting
- **🎯 Prompt Engineering** - Optimized prompts for research tasks

### Tool Integration

1. **🌐 Web Search** - [`DuckDuckGoSearchRun`](tools.py) for real-time web information
2. **📖 Wikipedia** - [`WikipediaQueryRun`](tools.py) for encyclopedia content
3. **💾 File Saver** - [`save_to_txt`](tools.py) for automatic output preservation

### Data Flow

1. **📝 Query Input** - User provides research topic or question
2. **🤖 Agent Processing** - LangChain agent analyzes query and selects appropriate tools
3. **� Information Gathering** - Tools execute searches and retrieve relevant data
4. **📊 Response Generation** - GPT-4o synthesizes information into structured output
5. **💾 Auto-Save** - Research results automatically saved to timestamped file
6. **📋 Structured Output** - Results returned in standardized ResearchResponse format

### Response Schema

```python
class ResearchResponse(BaseModel):
    topic: str              # Main research topic
    summary: str            # Comprehensive summary of findings
    sources: list[str]      # List of sources used
    tools_used: list[str]   # Tools utilized in research
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Git

### Environment Setup

1. **Clone the repository**

```bash
git clone https://github.com/Haythem532002/ai-search-agent.git
cd ai-search-agent
```

2. **Set up Python virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a [`.env`](.env) file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Application

**Start the research agent**

```bash
python main.py
```

The agent will automatically research the default query: "What is the capital of Tunisia"

### Customizing Queries

Modify the query in [`main.py`](main.py):

```python
raw_response = agent_executor.invoke(
    {"query": "Your research question here"})
```

### Example Usage

```python
# Example queries you can try:
queries = [
    "What are the latest developments in AI?",
    "Explain quantum computing basics",
    "What is the history of machine learning?",
    "How does blockchain technology work?"
]
```

## 📁 Project Structure

```
AI-Search-Agent/
├── main.py                        # Main application entry point
├── tools.py                       # Tool definitions and implementations
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore configuration
├── Research_Output.txt           # Generated research outputs
├── venv/                         # Python virtual environment
├── __pycache__/                  # Python cache files
└── README.md                     # Project documentation
```

## 🔧 Configuration

### Tool Customization

The [`tools.py`](tools.py) file contains three main tools:

- **[`search_tool`](tools.py)** - DuckDuckGo web search
- **[`wiki_tool`](tools.py)** - Wikipedia content retrieval
- **[`save_tool`](tools.py)** - File output with timestamps

### Agent Customization

Modify the system prompt in [`main.py`](main.py) to change the agent's behavior:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt here..."),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
])
```

### Output Customization

The [`ResearchResponse`](main.py) Pydantic model can be extended:

```python
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    confidence_score: float  # Add custom fields
    research_depth: str      # Add custom fields
```

## 🧪 Testing

### Run Basic Tests

```bash
# Test the agent with a simple query
python main.py

# Test individual tools
python -c "from tools import search_tool, wiki_tool, save_tool; print('Tools imported successfully')"

# Test OpenAI connection
python -c "from langchain_openai import ChatOpenAI; llm = ChatOpenAI(model='gpt-4o'); print('OpenAI connection OK')"
```

### Test Individual Components

```bash
# Test web search
python -c "from tools import search_tool; print(search_tool.run('Python programming'))"

# Test Wikipedia search
python -c "from tools import wiki_tool; print(wiki_tool.run('Artificial Intelligence'))"

# Test file saving
python -c "from tools import save_tool; print(save_tool.run('Test data'))"
```

### Custom Query Testing

```python
# Example test script
from main import agent_executor

test_queries = [
    "What is machine learning?",
    "History of the internet",
    "Climate change effects"
]

for query in test_queries:
    response = agent_executor.invoke({"query": query})
    print(f"Query: {query}")
    print(f"Response: {response}")
    print("-" * 50)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Install development dependencies (`pip install -r requirements.txt`)
4. Make your changes with proper tests
5. Commit your changes (`git commit -m 'Add AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for functions and classes
- Test new features before submitting
- Update documentation for new functionality
- Use conventional commits for clear history

### Adding New Tools

To add a new tool to the agent:

1. Create the tool in [`tools.py`](tools.py):

```python
def your_new_tool(query: str) -> str:
    # Your tool implementation
    return result

new_tool = Tool(
    name="YourTool",
    func=your_new_tool,
    description="Description of what your tool does"
)
```

2. Add it to the tools list in [`main.py`](main.py):

```python
tools = [search_tool, wiki_tool, save_tool, new_tool]
```

## 📊 Performance & Monitoring

- **⚡ Response Times**: Typical query response under 10-15 seconds
- **🎯 Accuracy**: High-quality responses with multi-source validation
- **💾 Storage**: Automatic research output persistence
- **🔍 Search Quality**: Dual-source information gathering (web + Wikipedia)
- **📝 Output Format**: Structured, validated responses with Pydantic

## 🔒 Security & Best Practices

- **� API Key Management**: Store OpenAI API key in `.env` file
- **📁 File Security**: Research outputs saved locally with timestamps
- **🛡️ Input Validation**: Pydantic models ensure data integrity
- **🚫 Rate Limiting**: Be mindful of OpenAI API usage limits
- **🔍 Search Safety**: DuckDuckGo provides safe web search results

## 📈 Future Enhancements

- 📄 **PDF Processing** - Add document ingestion capabilities
- 🗄️ **Database Integration** - Store research results in database
- 🌐 **Web Interface** - Add Flask/FastAPI web frontend
- 📊 **Analytics Dashboard** - Track research patterns and topics
- 🔄 **Batch Processing** - Process multiple queries simultaneously
- 🎯 **Source Ranking** - Implement source credibility scoring

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **🦜 LangChain** for the excellent agent framework and tool integration
- **🤖 OpenAI** for providing the powerful GPT-4o language model
- **🔍 DuckDuckGo** for privacy-focused web search capabilities
- **📚 Wikipedia** for comprehensive encyclopedia content
- **� Pydantic** for robust data validation and parsing

---

**Built with ❤️ using Modern AI & Agent Architecture**
