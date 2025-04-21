🚀AI Research Agent System
[Python Version: 3.9+] [License: MIT]

Features:
Dual-Agent Architecture:
 - 🕷️Research Agent: Web crawler using Tavily API
 - ✍️Answer Drafter: Structured summarization using Gemini

Intelligent Workflow:
 - ⚙️ LangGraph for agent orchestration
 - 🔗 LangChain for agent development

Professional Outputs:
 - 📝 Well-formatted research summaries
 - 📚 Proper source citations
 - 🧾 Clear section organization




📦 Installation
1. Clone the repository:
 git clone https://github.com/yourusername/deep-research-agent.git
 cd deep-research-agent

2. Create and activate virtual environment:
 Linux/macOS:
 python -m venv venv
 source venv/bin/activate
 Windows:
 python -m venv venv
 venv\Scripts\activate

3. Install dependencies:
 pip install -r requirements.txt

4. Set up environment variables:
 cp .env.example .env
 Edit .env with your API keys:
 TAVILY_API_KEY=your_tavily_key
 GEMINI_API_KEY=your_gemini_key


🛠️ Usage
**Run the research system:
 python main.py
 
🔍 Enter topic (or 'quit'): Explain quantum computing

🧠 Researching...
✅ Completed in 8.5s

📝 Final Answer:
==================================================
[Professional research summary with sources]
==================================================

🔧 Technologies Used
LangChain: Agent framework

LangGraph: Workflow orchestration

Tavily: Web research API

Google Gemini: LLM for summarization

Python 3.9+: Core programming language
