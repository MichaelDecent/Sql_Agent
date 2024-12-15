# main.py
from config.settings import set_env
import gradio as gr


# Define the function that sets up the environment
def setup_environment(database_url: str, api_key: str):
    set_env("OPENAI_API_KEY", api_key)
    set_env("DATABASE_URL", database_url)


# Define the function that processes the chat prompt
def process_chat(database_url: str = None, api_key: str = None, prompt: str = None):
    setup_environment(database_url, api_key)

    from workflows.workflow_setup import setup_workflow

    app = setup_workflow()

    messages = app.invoke({"messages": [("user", prompt)]})

    return messages["messages"][-1].tool_calls[0]["args"]["final_answer"]


# Create the Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            # Create input components for settings
            database_url = gr.Textbox(
                label="Database URL", placeholder="Enter the database URL", type="password"
            )
            api_key = gr.Textbox(
                label="API Key", placeholder="Enter the API Key", type="password"
            )
        with gr.Column(scale=4):
            # Create input and output components for chat
            prompt = gr.Textbox(
                label="Chat Prompt", placeholder="Enter your chat prompt"
            )
            response = gr.Textbox(label="Response")

            # Define the event listener for the chat prompt
            prompt.submit(process_chat, [database_url, api_key, prompt], response)

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch(show_error=True)
