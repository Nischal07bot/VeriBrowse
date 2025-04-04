import os
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph, END
from langchain.schema import SystemMessage
import base64
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BrowserAIAgent:
    def __init__(self, api_key=None):
        """
        Initialize the BrowserAIAgent with necessary components
        
        Args:
            api_key (str, optional): Google API key. If not provided, will try to get from environment
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or "AIzaSyBv-bggOuqBjfQWk3kfpDEX0LnfS0rGCms"
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Setup LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            max_output_tokens=1000,
            temperature=0.2,
            google_api_key=self.api_key
        )
        
        # Setup tools
        self.image_tool = Tool(
            name="ImageToBrowserAction",
            func=lambda x: self._image_to_action_tool(x["image_path"], x["task"]),
            description="Given an image of the browser and a task, suggest the next browser automation action."
        )
        
        # Setup memory
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        # Setup agent
        self.agent = initialize_agent(
            tools=[self.image_tool],
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            memory=self.memory,
            verbose=True,
        )
        
        # Setup workflow
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile()
    
    def _image_to_action_tool(self, image_path: str, task: str) -> str:
        """Process an image and return the next browser action"""
        try:
            with open(image_path, "rb") as f:
                img_bytes = f.read()
            b64_img = base64.b64encode(img_bytes).decode()
            
            msg = [
                SystemMessage(content="You are a browser automation agent. Analyze the image and give the next browser action."),
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64_img}"
                    }
                },
                {
                    "type": "text",
                    "text": f"Task: {task}"
                }
            ]
            response = self.llm.invoke(msg)
            return response.content
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return f"Error analyzing image: {str(e)}"
    
    def _create_workflow(self):
        """Create a LangGraph workflow"""
        class DevAgentState(dict):
            task: str
            image_path: str
            action: str
            complete: bool = False
        
        def decide_action(state):
            print("Processing image to get next action...")
            action = self.agent.run({"image_path": state["image_path"], "task": state["task"]})
            return DevAgentState({
                **state,
                "action": action,
            })
        
        workflow = StateGraph(DevAgentState)
        workflow.add_node("decide_action", decide_action)
        workflow.set_entry_point("decide_action")
        workflow.add_edge("decide_action", END)
        return workflow
    
    async def process_query(self, query, image_path="image.png"):
        """
        Process a query asynchronously
        
        Args:
            query (str): The user's task or query
            image_path (str): Path to the screenshot image
            
        Returns:
            str: The suggested browser action
        """
        try:
            result = self.app.invoke({"task": query, "image_path": image_path})
            return result["action"]
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return f"Error processing your request: {str(e)}"
    
    def process_query_sync(self, query, image_path="image.png"):
        """
        Process a query synchronously
        
        Args:
            query (str): The user's task or query
            image_path (str): Path to the screenshot image
            
        Returns:
            str: The suggested browser action
        """
        try:
            result = self.app.invoke({"task": query, "image_path": image_path})
            return result["action"]
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return f"Error processing your request: {str(e)}"

# For testing directly
if __name__ == "__main__":
    # Create an instance of the agent
    agent = BrowserAIAgent()
    
    # Test with a sample query
    task = "Find the price of iPhone from the flipkart."
    image_path = "image.png"  # Path to your screenshot image
    
    result = agent.process_query_sync(task, image_path)
    print("Next action suggestion:", result)
