from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from tools import search_tool, wiki_tool, save_tool
import json
import logging
import re

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Allow the Next.js dev server to call this API during development
# Adjust origins in production as needed.
CORS(app, resources={r"/research": {"origins": ["http://localhost:3000"]}})


# ===== LLM =====
llm = OllamaLLM(model="mistral")

# ===== Tools =====
tools = [search_tool, wiki_tool, save_tool]


# ===== Structured Chat Agent =====
# Note: building the agent at import time keeps the endpoint simple.
agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
)


def _extract_json_from_text(text: str) -> dict:
    """Try several strategies to extract JSON from arbitrary LLM text.

    Returns parsed JSON (dict) or raises ValueError.
    """
    # Fast path: text already looks like JSON
    text = text.strip()
    if not text:
        raise ValueError("Empty text")

    # If it already starts with { or [ try direct load
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find the first {...} block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except Exception:
            # fallthrough
            pass

    # Last resort: attempt to repair simple mistakes like single quotes
    repaired = text.replace("'", '"')
    try:
        return json.loads(repaired)
    except Exception:
        pass

    # If nothing works, raise
    raise ValueError("Unable to parse JSON from agent output")


def parse_agent_result(result) -> dict:
    """Normalize agent.invoke result to a JSON-serializable dict.

    Handles common shapes:
    - result is {'output': {...}} or {'output': '...json...'}
    - result is {'output': [{'text': '...json...'}]}
    """
    if not isinstance(result, dict):
        raise ValueError("Unexpected agent result type: %s" % type(result))

    output = result.get("output")

    # Direct dict
    if isinstance(output, dict):
        return output

    # If output is a list, look for first dict or string
    if isinstance(output, list) and output:
        # Try to find a dict element first
        for item in output:
            if isinstance(item, dict):
                return item
            if isinstance(item, str):
                try:
                    return _extract_json_from_text(item)
                except ValueError:
                    continue

        # If list contains objects with 'text' field
        for item in output:
            if isinstance(item, dict) and "text" in item:
                t = item.get("text")
                if isinstance(t, str):
                    try:
                        return _extract_json_from_text(t)
                    except ValueError:
                        continue

    # If output is a string try to parse
    if isinstance(output, str):
        return _extract_json_from_text(output)

    # Nothing worked
    raise ValueError("Could not extract JSON from agent result")


@app.get("/research")
def research():
    user_query = request.args.get("query")

    if not user_query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    prompt = (
        "You are a research agent. Use tools if needed.\n\n"
        "Your FINAL answer must be ONLY this JSON:\n\n"
        "{\n  \"topic\": \"string\",\n  \"summary\": \"string\",\n  \"sources\": [\"url1\", \"url2\"],\n  \"tools_used\": [\"tool1\", \"tool2\"]\n}\n\n"
        "No markdown. No other text."
    )

    try:
        result = agent.invoke({"input": prompt + "\nQuery: " + user_query})
        logger.info("Agent invoked for query: %s", user_query)
    except Exception as e:
        logger.exception("Agent invocation failed")
        return jsonify({"error": "Agent invocation failed", "detail": str(e)}), 500

    try:
        parsed = parse_agent_result(result)
        # Log the parsed structure for debugging unexpected shapes
        logger.info("Parsed agent result keys: %s", list(parsed.keys()) if isinstance(parsed, dict) else type(parsed))
    except Exception as e:
        logger.exception("Failed to parse agent result")
        # Include raw result for debugging (be careful with sensitive data)
        return (
            jsonify({"error": "Invalid JSON from agent", "detail": str(e), "raw": result}),
            500,
        )

    # Normalize parsed response to a simple, predictable shape for the frontend
    try:
        if not isinstance(parsed, dict):
            normalized = {
                "topic": None,
                "summary": str(parsed),
                "sources": [],
                "tools_used": [],
            }
        else:
            # try several common key names
            topic = parsed.get("topic") or parsed.get("Topic") or parsed.get("title") or parsed.get("Title")
            summary = (
                parsed.get("summary")
                or parsed.get("Summary")
                or parsed.get("answer")
                or parsed.get("text")
                or ""
            )

            # normalize sources into a list
            sources = []
            raw_sources = parsed.get("sources") if "sources" in parsed else parsed.get("source")
            if isinstance(raw_sources, list):
                sources = raw_sources
            elif isinstance(raw_sources, str) and raw_sources:
                # single string source -> wrap
                sources = [raw_sources]

            # normalize tools_used into a list
            tools_used = []
            raw_tools = parsed.get("tools_used") if "tools_used" in parsed else parsed.get("tools")
            if isinstance(raw_tools, list):
                tools_used = raw_tools
            elif isinstance(raw_tools, str) and raw_tools:
                tools_used = [raw_tools]

            normalized = {
                "topic": topic,
                "summary": summary,
                "sources": sources,
                "tools_used": tools_used,
                # include raw parsed for debugging in frontend if needed
                "_raw_parsed": parsed,
            }
    except Exception:
        normalized = {"topic": None, "summary": "", "sources": [], "tools_used": [], "_raw_parsed": parsed}

    # Optionally: run save_tool to persist result (if you want automatic saving)
    try:
        # If save_tool is a Tool wrapper (langchain Tool) it may expect .run or .func
        payload = json.dumps(normalized)
        if hasattr(save_tool, "run"):
            save_tool.run(payload)
        elif hasattr(save_tool, "func"):
            save_tool.func(payload)
        else:
            # fallback: call directly if it's a plain function
            try:
                save_tool(payload)
            except Exception:
                pass
    except Exception:
        logger.exception("Failed to save result (non-fatal)")

    return jsonify(normalized)


if __name__ == "__main__":
    # Debug use only. For production use gunicorn/uvicorn + process manager.
    app.run(port=5001, debug=True)
