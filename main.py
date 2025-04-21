from langgraph.graph import Graph
from agents.research_agent import ResearchAgent
from agents.draft_agent import DraftAgent
from dotenv import load_dotenv
import os
import time

load_dotenv()

def main():
    print("🚀 AI Research System (Gemini 1.5 Pro) Initializing...\n")
    
    try:
        print("🔧 Loading components...")
        research_agent = ResearchAgent()
        draft_agent = DraftAgent()
        
        print("⚙️ Creating workflow...")
        workflow = Graph()
        workflow.add_node("research", research_agent.research)
        workflow.add_node("draft", draft_agent.draft_answer)
        workflow.add_edge("research", "draft")
        workflow.set_entry_point("research")
        workflow.set_finish_point("draft")
        
        app = workflow.compile()
        print("✅ System ready!\n")
        
        while True:
            topic = input("\n🔍 Enter topic (or 'quit'): ").strip()
            if topic.lower() == 'quit':
                break
            if not topic:
                print("⚠️ Please enter a valid topic")
                continue
            
            print("\n🧠 Researching...")
            start_time = time.time()
            
            try:
                # The key fix is here - we need to properly handle the output
                result = app.invoke({"input": topic})
                
                # The draft output is actually in result["draft"]["output"]
                if isinstance(result, dict) and "draft" in result:
                    if isinstance(result["draft"], dict):
                        final_output = result["draft"].get("output", "")
                    else:
                        final_output = str(result["draft"])
                    
                    print(f"\n✅ Completed in {time.time()-start_time:.1f}s")
                    print("\n📝 Final Answer:")
                    print("=" * 50)
                    print(final_output)
                    print("=" * 50)
                    continue
                
                # If we get here, try to find the output in other possible locations
                final_output = result.get("output", "") if isinstance(result, dict) else str(result)
                
                if not final_output:
                    print("\n❌ Error: The system worked but couldn't find the output")
                    print("Here's the raw result for debugging:")
                    print(result)
                else:
                    print(f"\n✅ Completed in {time.time()-start_time:.1f}s")
                    print("\n📝 Final Answer:")
                    print("=" * 50)
                    print(final_output)
                    print("=" * 50)
                    
            except Exception as e:
                print(f"\n🔥 Processing error: {str(e)}")
                
    except Exception as e:
        print(f"\n💥 System failure: {str(e)}")

if __name__ == "__main__":
    main()