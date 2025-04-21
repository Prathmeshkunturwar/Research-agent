from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

class DraftAgent:
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro-latest",
                temperature=0.3,
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
            
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a professional editor. Create:
                1. Clear introduction
                2. Bullet-point key findings
                3. Source references
                4. Short conclusion
                
                Return ONLY the formatted content, nothing else."""),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            self.agent = create_tool_calling_agent(self.llm, [], self.prompt)
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=[],
                verbose=True,
                handle_parsing_errors=True,
                return_intermediate_steps=False
            )
        except Exception as e:
            print(f"🔴 DraftAgent error: {str(e)}")
            raise

    def draft_answer(self, research_data):
        try:
            if isinstance(research_data, dict):
                if research_data.get("status") != "success":
                    return {"status": "error", "message": research_data.get("message", "Research failed")}
                content = research_data.get("data", "")
            else:
                content = str(research_data)
            
            result = self.agent_executor.invoke({"input": f"Format this research:\n{content}"})
            return {"output": result.get("output", "")}  # Ensure we return a dict with "output" key
        except Exception as e:
            return {"output": f"Error in drafting: {str(e)}"}