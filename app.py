import streamlit as st
import os
from src.chatbot import create_chatbot
from src.utils import load_api_key
from IPython.display import Image
import io

# Load OpenAI API key
api_key = load_api_key()
if api_key:
  os.environ["OPENAI_API_KEY"] = api_key

# Create chatbot
graph = create_chatbot()

st.title("Multi-Agent Chatbot with External Tools")

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
  st.markdown(message["content"])

# React to user input
prompt = st.text_input("What is your question?")
if st.button("Send"):
  if prompt:
      # Display user message
      st.markdown("=" * 32 + " Human Message " + "=" * 32)
      st.markdown(prompt)
      st.session_state.messages.append({"role": "user", "content": f"{'=' * 32} Human Message {'=' * 32}\n\n{prompt}"})

      # Get bot response
      events = graph.stream(
          {"messages": [("user", prompt)]},
          stream_mode="values"
      )
      
      full_response = ""
      tool_message = ""
      for event in events:
          message = event["messages"][-1]
          if hasattr(message, 'type') and message.type == "tool":
              tool_message += f"Name: {message.name}\n\n{message.content}\n"
          elif hasattr(message, 'type') and message.type == "function":
              st.markdown("=" * 34 + " Ai Message " + "=" * 34)
              st.markdown(f"Tool Calls:\n  {message.name} ({message.id})\n Call ID: {message.id}\n  Args:\n    query: {message.args['query']}")
          else:
              full_response += message.content

      if tool_message:
          st.markdown("=" * 33 + " Tool Message " + "=" * 33)
          st.markdown(tool_message)
      
      st.markdown("=" * 34 + " Ai Message " + "=" * 34)
      formatted_response = f"User: {prompt}\n\nAI: {full_response.strip()}\n"
      st.markdown(formatted_response)
      
      # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": f"{'=' * 34} Ai Message {'=' * 34}\n\n{formatted_response}"})

# Add a section for OpenAI API key input
st.sidebar.title("Configuration")
new_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Update the OpenAI API key
if new_api_key:
  os.environ["OPENAI_API_KEY"] = new_api_key
  st.sidebar.success("API key set successfully!")
else:
  st.sidebar.warning("Please enter your OpenAI API key to use the chatbot.")

# Display the graph in the sidebar
st.sidebar.title("LangGraph")
try:
  graph_image = graph.get_graph().draw_mermaid_png()
  st.sidebar.image(graph_image, use_column_width=True)
except Exception as e:
  st.sidebar.error(f"Failed to display graph: {str(e)}")