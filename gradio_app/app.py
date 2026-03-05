import pandas as pd
import requests
import random
import gradio as gr

# Ollama API URL
OLLAMA_API = "http://host.docker.internal:11434/api/generate"

# Load CSV
df = pd.read_csv("past_emails.csv")

def generate_reply(incoming_email):
    # Sample 10 emails for style reference
    style_emails = df['body_formatted'].dropna().sample(min(10, len(df))).tolist()
    style_text = "\n\n".join(style_emails)

    prompt = f"""
You are my personal email assistant and answer to HR people who are reaching out to me regarding applications and jobs.
The task:
You will give a positive answer to the incoming email, touch upon the key points from the mail and so on. Make sure that you adapt the tone, phrasing, and style of my previous emails. The answer should sound like it was written by me. Please answer in the language that the incoming email is written in. Write around 200-500 characters, depending on the bespoken topics in the incoming email. If there are no specific topics, write around 200 characters. Write out of the perspective of me, who the incoming mail was sent to.
The no-gos:
Don't copy and paste sentences from the previous emails. Don't answer a novel. Don't mimic the incoming email, but instead answer to it.

Incoming email:
{incoming_email}

My previous emails:
{style_text}
"""

    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "prompt": prompt,
                #"model": "mistral", --to high CPU usage, switched to smaller model and GPU-friendly
                "model": "llama3.2:3b",  
                "max_tokens": 250,
                "temperature": 0.7,
                "max_tokens": 250,
                "stream": False
            }
        )
        if response.status_code != 200:
            return f"Error: {response.text}"
        return response.json().get("response", "")
    except Exception as e:
        return f"Error connecting to Ollama API: {e}"

# Gradio UI
ui = gr.Interface(
    fn=generate_reply,
    inputs=gr.Textbox(lines=12, label="Incoming Email"),
    outputs=gr.Textbox(lines=12, label="Generated Reply"),
    title="Email Reply Generator"
)

ui.launch(server_name="0.0.0.0", server_port=7860)