from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro-latest",
                temperature=0.5,
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
            
            self.tools = [TavilySearchResults(max_results=3)]
            
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert research assistant. For any query:
                1. Find 3 authoritative sources
                2. Extract key facts with source URLs
                3. Return in format:
                - [Fact 1](URL1)
                - [Fact 2](URL2)
                - [Fact 3](URL3)"""),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=3,
                return_intermediate_steps=True  # Added this line
            )
        except Exception as e:
            print(f"🔴 ResearchAgent error: {str(e)}")
            raise

    def research(self, input_data):
        try:
            if isinstance(input_data, dict):
                topic = input_data.get("input", "")
            else:
                topic = str(input_data)
                
            result = self.agent_executor.invoke({"input": f"Research: {topic}"})
            return {"status": "success", "data": result.get("output", "")}
        except Exception as e:
            return {"status": "error", "message": str(e)}