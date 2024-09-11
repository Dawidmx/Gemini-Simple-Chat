import os
import time
import json
from typing import List, Tuple, Dict, Union

import google.generativeai as genai
import gradio as gr

# settings
temperature = 0
max_output_tokens = 8192
stop_sequences = ["STOP", "END"]
top_k = 1
top_p = 0
safety_settings = {
    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
}

os.environ['COMMANDLINE_ARGS'] = "--no-gradio-queue"
print("google-generativeai:", genai.__version__)

# Your API Key
gapi = "XYZ"  


CHAT_HISTORY = List[Union[Tuple[str, str], Tuple[Tuple[str, str], str]]]

def load_prompt_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

GP0 = load_prompt_from_file('file.txt')

def preprocess_chat_history(history: CHAT_HISTORY) -> List[Dict[str, Union[str, List[str]]]]:
    messages = []
    for user_message, assistant_message in history:
        if isinstance(user_message, tuple):
            pass  # Image messages not supported in this example
        elif user_message is not None:
            messages.append({'role': 'user', 'parts': [user_message]})
        if isinstance(assistant_message, tuple):
            pass  # Image messages not supported in this example
        elif assistant_message is not None:
            messages.append({'role': 'model', 'parts': [assistant_message]})
    return messages

def save_chat(chatbot: CHAT_HISTORY, filename: str):
    with open(filename, "w") as f:
        json.dump(chatbot, f)

def load_chat(filename: str) -> CHAT_HISTORY:
    with open(filename, "r") as f:
        return json.load(f)

def delete_last_message(chatbot: CHAT_HISTORY):
    if len(chatbot) > 0:
        chatbot.pop()
    return chatbot

def user(text_prompt: str, chatbot: CHAT_HISTORY):
    if text_prompt:
        chatbot.append((text_prompt, None))
    else:
        if len(chatbot) > 0:
            chatbot[-1] = (chatbot[-1][0], None)
    return "", chatbot

def bot(chatbot: CHAT_HISTORY):
    if len(chatbot) == 0 or chatbot[-1][1] is not None:
        return chatbot

    preprocessed_history = preprocess_chat_history(chatbot)

    genai.configure(api_key=gapi)
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_k=top_k,
        top_p=top_p,
    )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0827",
        system_instruction=GP0
    )

    corrected_response = model.generate_content(
        preprocessed_history,
        request_options={"timeout": 600},
        stream=True,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    chatbot[-1] = list(chatbot[-1])
    chatbot[-1][1] = ""
    for chunk in corrected_response:
        for i in range(0, len(chunk.text), 10):
            section = chunk.text[i:i + 10]
            chatbot[-1][1] += section
            time.sleep(0.01)
            yield chatbot
    chatbot[-1] = tuple(chatbot[-1])

#Gradio
chatbot_component = gr.Chatbot(
    label='Gemini',
    bubble_full_width=False,
    scale=2,
    height=700
)
delete_button_component = gr.Button(value="Delete last message", variant="secondary", scale=0.03)
save_button_component = gr.Button(value="Save Chat")
load_button_component = gr.Button(value="Load Chat")
filename_component = gr.Textbox(label="File name", value="chat1.json")

with gr.Blocks(css=".gradio-container { height: 100vh; }") as demo:
    with gr.Row():
        with gr.Column(scale=1):
            delete_button_component.render()
            save_button_component.render()
            load_button_component.render()
            filename_component.render()
        with gr.Column(scale=3):
            chatbot_component.render()
            with gr.Row():
                text_prompt_component = gr.Textbox(
                    placeholder="Type your message...",
                    show_label=False,
                    autofocus=True,
                    scale=8
                )
                run_button_component = gr.Button(value="Send", variant="primary", scale=1)
                text_prompt_component, run_button_component

    run_button_component.click(
        fn=user,
        inputs=[text_prompt_component, chatbot_component],
        outputs=[text_prompt_component, chatbot_component],
        queue=False
    ).then(
        fn=bot,
        inputs=[chatbot_component],
        outputs=[chatbot_component],
    )
    delete_button_component.click(
        fn=delete_last_message,
        inputs=[chatbot_component],
        outputs=[chatbot_component],
        queue=False
    )
    save_button_component.click(
        fn=save_chat,
        inputs=[chatbot_component, filename_component],
        outputs=[],
    )
    load_button_component.click(
        fn=load_chat,
        inputs=[filename_component],
        outputs=[chatbot_component],
    )

demo.queue(max_size=99).launch(debug=False, show_error=True)