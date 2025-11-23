from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from tools import search_tool, wiki_tool, save_tool
import json

app = Flask(__name__)
load_dotenv()

# ===== LLM =====
llm = OllamaLLM(model="mistral")

# ===== Tools =====
tools = [search_tool, wiki_tool, save_tool]

# ===== FIXED: Use Zero-Shot ReAct (NOT structured chat) =====
agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # FIX
    verbose=False,
    handle_parsing_errors=True  # IMPORTANT FIX
)

# ===== API Route =====
@app.get("/research")
def research():
    user_query = request.args.get("query")

    if not user_query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    prompt = """
    You are a research agent. Use tools if needed.

    Respond ONLY in this JSON format:

    {
      "topic": "string",
      "summary": "string",
      "sources": ["url1", "url2"],
      "tools_used": ["tool1", "tool2"]
    }

    No markdown. No explanation. No code blocks.
    """

    # Run agent
    result = agent.invoke({
        "input": prompt + "\nQuery: " + user_query
    })

    output = result.get("output", "")

    # Try to parse JSON
    try:
        parsed = json.loads(output)
        return jsonify(parsed)
    except:
        # If model adds text around JSON, extract JSON using regex
        import re
        json_match = re.search(r"\{[\s\S]*\}", output)
        if json_match:
            try:
                return jsonify(json.loads(json_match.group(0)))
            except:
                pass

        return jsonify({"error": "Model output is not valid JSON", "raw": output}), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
