from flask import Flask, render_template, request, jsonify
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGoTools()],
    instructions="Always include the sources",
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Analyze financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, 
                         stock_fundamentals=True, company_info=True)],
    instructions="Use tables to display financial data",
    show_tool_calls=True,
    markdown=True,
)

def route_query(user_input):
    finance_keywords = ["stock", "finance", "market", "investment", "company analysis", "share price"]

    if any(keyword in user_input.lower() for keyword in finance_keywords):
        response = finance_agent.run(user_input)
    else:
        response = web_agent.run(user_input)

    print("=== DEBUG: response type ===", type(response))
    print("=== DEBUG: response value ===", response)

    if isinstance(response, str):
        return response
    elif isinstance(response, dict):
        return response.get("content") or response.get("text") or str(response)
    elif hasattr(response, 'content'):  
        return response.content
    elif hasattr(response, '__str__'):
        return str(response)
    else:
        return "Unexpected response format received."
    
from markupsafe import Markup

def format_response_as_html(text):
    if not isinstance(text, str):
        return Markup(str(text))

    html = ""
    lines = text.strip().splitlines()

    for line in lines:
        if line.startswith("### "):
            html += f"<h3 class='text-xl font-semibold mt-4 mb-2'>{line[4:].strip()}</h3>"
        elif line.startswith("* "):
            if "<ul>" not in html[-10:]:
                html += "<ul class='list-disc pl-5 mb-2'>"
            html += f"<li class='mb-1'>{line[2:].strip()}</li>"
        elif line.startswith("Sources:") or "Sources:" in line:
            html += "<h4 class='text-lg font-semibold mt-4 mb-1'>Sources:</h4><ul class='list-disc pl-5'>"
        elif line.startswith("* ["):
            # Format Markdown-style link: * [Label](URL)
            start = line.find('[') + 1
            end = line.find(']')
            label = line[start:end]
            url = line[line.find('(')+1 : line.find(')')]
            html += f"<li><a href='{url}' class='text-blue-600 underline' target='_blank'>{label}</a></li>"
        else:
            html += f"<p class='mb-2'>{line.strip()}</p>"

    if "</ul>" not in html:
        html += "</ul>"

    return Markup(html)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message', '').strip()

    if not user_input:
        return jsonify({"error": "Empty message received"}), 400  

    try:
        response = route_query(user_input)
        beautified_response = format_response_as_html(response)
        return jsonify({"response": beautified_response})  

    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
if __name__ == '__main__':
    app.run(debug=True)
