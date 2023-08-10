# Object Generator README

Welcome to the documentation for the Object Generator. This app is designed to transcribe videos and generate summaries for the transcriptions using the GPT-3.5-turbo model. Below are the instructions on how to use the app effectively.

**Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Setting up the OpenAI API key](#setting-up-the-openai-api-key)
4. [Using the App](#using-the-app)
5. [Note on Cost](#note-on-cost)
6. [Customizing Prompt Templates](#customizing-prompt-templates)

## Prerequisites

Before using the app, make sure you have the following:

1. An OpenAI API key: Obtain your OpenAI API key from the [OpenAI website](https://openai.com).
2. Python: The app is written in Python, so you should have Python installed on your system.

## Installation

1. Clone the repository: 
   ```
   git clone [repository_url]
   ```
2. Install the required Python packages: 
   ```
   pip install -r requirements.txt
   ```

## Setting up the OpenAI API key

1. Open the `main.py` file in a text editor.
2. Locate the line: `os.environ["OPENAI_API_KEY"] = ""` and replace the empty quotes with your actual OpenAI API key.

## Using the App

The app provides a simple command-line interface to perform two main tasks: video transcription and generating summaries for the transcripts. Follow the steps below to use the app:

1. Organize your videos and transcripts:
   - Place the videos you want to transcribe in the `videos` folder.
   - If you already have transcript files, place them in the `transcripts` folder. Each transcript should be in a separate text file.

2. Run the app:
   - Open a terminal or command prompt.
   - Navigate to the app's directory.

3. Execute the `app.py` script:
   ```
   python app.py
   ```

4. The app will display a menu with the following options:

   - **1. Transcribe video(s)**: Choose this option to transcribe one or more videos. You will be prompted to enter the video number(s) you want to transcribe (comma-separated).
   
   - **2. Generate summary for transcript(s)**: Choose this option to generate summaries for existing transcripts. You will be prompted to enter the transcript number(s) for which you want to generate summaries (comma-separated).
   
   - **3. Transcribe video(s) and generate summary**: This option combines video transcription and summary generation. You will first transcribe the selected video(s) and then generate summaries for the corresponding transcripts.
   
   - **4. Exit**: Choose this option to exit the app.

## Note on Cost

The app utilizes the OpenAI API for generating summaries, which may incur costs based on your usage. The cost will depend on the number and length of interactions with the API. You can check the total cost of API calls in the terminal after running the app.

## Customizing Prompt Templates

The app uses prompt templates to interact with the GPT-3.5-turbo model. If you wish to customize the prompts used for summarization, you can modify the `prompt_inter_template` and `prompt_final_template` variables in the `main.py` file.

---
