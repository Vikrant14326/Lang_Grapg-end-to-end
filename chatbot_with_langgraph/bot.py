import os
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, Literal, TypedDict
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

class chatbot:
    def __init__(self):
        # Initialize the ChatGroq model with the API key
        self.llm = ChatGroq(model_name="Gemma2-9b-It", api_key="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")
        
    def call_tool(self):
        # Check if the tavily_api_key is set correctly via environment variable or hardcoded
        tavily_api_key = os.getenv("TAVILY_API_KEY", "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")  # Default to a hardcoded key if not set
        
        if not tavily_api_key:
            raise ValueError("Tavily API key not found. Ensure it's set as an environment variable or passed as a parameter.")
        
        # Initialize TavilySearchResults with the API key
        tool = TavilySearchResults(max_results=2, tavily_api_key=tavily_api_key)
        
        # Create a ToolNode and bind it with the LLM model
        tools = [tool]
        self.tool_node = ToolNode(tools=[tool])
        self.llm_with_tool = self.llm.bind_tools(tools)
        
    def call_model(self, state: MessagesState):
        # Extract messages from the state and pass them to the model for response
        messages = state['messages']
        response = self.llm_with_tool.invoke(messages)
        return {"messages": [response]}
    
    def router_function(self, state: MessagesState) -> Literal["tools", END]:
        # Check the last message and route accordingly
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END
    
    def __call__(self):
        # Set up the workflow
        self.call_tool()
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tool_node)
        
        # Define the flow of messages between nodes
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", self.router_function, {"tools": "tools", END: END})
        workflow.add_edge("tools", 'agent')
        
        # Compile the workflow and return the app
        self.app = workflow.compile()
        return self.app
        
if __name__ == "__main__":
    # Initialize and invoke the chatbot workflow
    mybot = chatbot()
    workflow = mybot()
    response = workflow.invoke({"messages": ["Who is the current prime minister of the USA?"]})
    
    # Print the final response
    print(response['messages'][-1].content)
