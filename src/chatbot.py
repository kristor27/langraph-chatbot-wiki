from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from .tools import tools

class State(TypedDict):
  messages: Annotated[list, add_messages]

def create_chatbot():
  graph_builder = StateGraph(State)
  
  llm = ChatOpenAI(model_name="gpt-3.5-turbo")
  llm_with_tools = llm.bind_tools(tools=tools)

  def chatbot(state: State):
      return {"messages": [llm_with_tools.invoke(state["messages"])]}

  graph_builder.add_node("chatbot", chatbot)
  tool_node = ToolNode(tools=tools)
  graph_builder.add_node("tools", tool_node)

  graph_builder.add_conditional_edges(
      "chatbot",
      tools_condition,
  )
  graph_builder.add_edge("tools", "chatbot")
  graph_builder.add_edge(START, "chatbot")

  return graph_builder.compile()