# Gemini Chat Application

This repository contains a Python-based chat application that uses Google's Gemini AI model. The application provides a Gradio interface for interacting with the AI model.

## Prerequisites

Before running this application, make sure you have Python installed on your system. This project was developed with Python 3.8+.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Dawidmx/Gemini-Simple-Chat.git
   cd Gemini-Simple-Chat
   ```

2. Install the required libraries:
   ```
   pip install google-generativeai gradio
   ```

## Configuration

1. API Key: Replace `"XYZ"` in the `gapi` variable with your actual Google API key.

2. Settings: The main settings for the Gemini model are located at the beginning of the script:
   ```python
   temperature = 0
   max_output_tokens = 8192
   stop_sequences = ["STOP", "END"]
   top_k = 1
   top_p = 0
   ```
   You can adjust these values as needed.

3. System Instructions: The system instructions are loaded from a file named `file.txt`. Make sure this file exists in the same directory as the script and contains your desired system instructions.

4. Gemini Model Version: To change the Gemini model version, locate the following line in the `bot` function:
   ```python
   model_name="gemini-1.5-pro-exp-0827"
   ```
   Replace `"gemini-1.5-pro-exp-0827"` with your desired model version.

## Usage

1. Run the script:
   ```
   python Gemini-Simple-Chat.py
   ```

2. Open the provided URL in your web browser to access the Gradio interface.

3. Type your messages in the text box and click "Send" to interact with the AI.

4. Use the "Delete last message", "Save Chat", and "Load Chat" buttons to manage your conversation history.

## Features

- Interactive chat interface
- Ability to save and load chat history
- Option to delete the last message
- Customizable AI model settings
