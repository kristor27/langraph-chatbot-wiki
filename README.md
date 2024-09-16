# LangGraph Chatbot with External Tools

This project implements a multi-agent chatbot using LangGraph, LangChain, and OpenAI's GPT model. The chatbot can access external tools like Wikipedia and ArXiv to provide more informed responses.

## Features

- Interactive chat interface using Streamlit
- Integration with OpenAI's GPT model
- Access to Wikipedia and ArXiv as external knowledge sources
- Streaming responses for a more dynamic user experience

## Installation

1. Clone this repository:
git clone https://github.com/yourusername/langraph-chatbot.git
cd langraph-chatbot


2. Create a virtual environment and activate it:
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate


3. Install the required dependencies:
pip install -r requirements.txt


4. Set up your OpenAI API key:
   - Rename `.env.example` to `.env`
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

Run the Streamlit app:
streamlit run app.py


Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Project Structure

- `app.py`: The main Streamlit application file
- `src/chatbot.py`: Contains the LangGraph chatbot implementation
- `src/tools.py`: Defines the external tools (Wikipedia and ArXiv)
- `src/utils.py`: Utility functions for the project

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.