import os
import whisper
import openai
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import TokenTextSplitter
from langchain.callbacks import get_openai_callback

os.environ["OPENAI_API_KEY"] = ""  # Place your OpenAI API key here

# Initialize the GPT-3.5-turbo model and other components
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=100)

# Define the prompt templates for summarization
prompt_inter_template = """Context: You are a professor of a class, and you have saved a transcript of your class lecture. You want to help your students summarize the topics you've covered into a list of key learning objects and objectives.

Text: 
{text}

Task: Using the given transcript text, provide a list of the key learning objects in the lecture. The following is an example of how to format each learning object in the list:
1. Main Topic 1: Learning objective
    a. Sub-topic 1: Learning objective
2. Main Topic 2: Learning objective
    a. Sub-topic 1: Learning objective
    ...
"""

prompt_final_template = """Context: Your job is to produce a final list of learning objects for a course lecture
    
The following lists are all the learning objects we have:
{text}
    
Task: Keep the same order of the given learning objects, however group any overarching concepts while still including the secondary objects that are more specific to the original learning objects. The following is an example of how to format each learning object in the list:
    1. Main Topic 1: Learning objective
        a. Sub-topic 1: Learning objective
    2. Main Topic 2: Learning objective
        a. Sub-topic 1: Learning objective
        ...
"""

PROMPT_INTER = PromptTemplate(template=prompt_inter_template, input_variables=["text"])
PROMPT_FINAL = PromptTemplate(template=prompt_final_template, input_variables=["text"])

# Function to transcribe a video and save the transcript
def transcribe_video(input_file: str):
    # Transcribe the video using the whisper library
    path = "./videos/" + input_file
    model = whisper.load_model("base.en")
    print(f"Transcribing {input_file}")
    result = model.transcribe(path)

    # Save the transcript to a text file
    output_file = f"./transcripts/transcript_{input_file}.txt"
    print(f"Creating txt file: {output_file}")
    with open(output_file, 'w') as f:
        f.write(result["text"])
    print(f"Completed {input_file}")
    return output_file

# Function to generate the summary for a transcript
def generate_summary(input_file: str, output_file: str):
    # Read the transcript text from the input file
    with open(input_file) as file:
        text = file.read()

    # Split the text into chunks to fit GPT-3.5-turbo's token limit
    texts = splitter.split_text(text)

    # Create Document objects for each chunk of the transcript
    docs = [Document(page_content=t) for t in texts]

    # Load the summarization chain
    chain = load_summarize_chain(llm, 
                                chain_type="map_reduce",
                                verbose=True,
                                map_prompt=PROMPT_INTER, 
                                combine_prompt=PROMPT_FINAL)

    # Set the prompt templates for the chain
    chain.llm_chain.prompt = PROMPT_INTER
    chain.combine_document_chain.llm_chain.prompt = PROMPT_FINAL

    total_cost = 0
    with get_openai_callback() as cb:
        print("Saving:" + input_file)
        # Generate the summary using the chain
        output_summary = chain.run(docs)

        # Write the summary and cost to the output file
        with open(output_file, 'a') as f:
            f.write(input_file + " Learning Objects\n" + output_summary + "\n" + "Cost: " + str(cb.total_cost) + "\n\n")
        total_cost += cb.total_cost
        print("Saved")
    print("Total Cost: "+ str(total_cost))
    return output_file

# Function to handle the main user interface
def main():
    # Get the list of available videos and transcripts
    videofiles = os.listdir('videos')
    transcripts = os.listdir('transcripts')

    while True:
        print("Menu:")
        print("1. Transcribe video(s)")
        print("2. Generate summary for transcript(s)")
        print("3. Transcribe video(s) and generate summary")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            # Option to transcribe video(s)
            videofiles = os.listdir('videos')  # Refresh the list of videos
            print("Available videos:")
            for idx, video in enumerate(videofiles, 1):
                print(f"{idx}. {video}")

            video_choice = input("Enter the video number(s) to transcribe (comma-separated, 0 to go back): ")
            if video_choice == '0':
                continue
            video_numbers = [int(num) for num in video_choice.split(",") if num.isdigit()]
            selected_videos = [videofiles[num - 1] for num in video_numbers if 1 <= num <= len(videofiles)]
            for video_file in selected_videos:
                transcribe_video(video_file)

        elif choice == '2':
            # Option to generate summary for transcript(s)
            transcripts = os.listdir('transcripts')  # Refresh the list of transcripts
            print("Available transcripts:")
            for idx, transcript in enumerate(transcripts, 1):
                print(f"{idx}. {transcript}")

            transcript_choice = input("Enter the transcript number(s) to generate summary (comma-separated, 0 to go back): ")
            if transcript_choice == '0':
                continue
            transcript_numbers = [int(num) for num in transcript_choice.split(",") if num.isdigit()]
            selected_transcripts = [f'transcripts/{transcripts[num - 1]}' for num in transcript_numbers if 1 <= num <= len(transcripts)]

            # Ask the user to input the output file name
            output_file_name = input("Enter the desired output file name (without extension): ")
            output_file = f"./learningobjects/{output_file_name}.txt"

            for transcript_file in selected_transcripts:
                generate_summary(transcript_file, output_file)

        elif choice == '3':
            # Option to transcribe video(s) and generate summary
            videofiles = os.listdir('videos')  # Refresh the list of videos
            print("Available videos:")
            for idx, video in enumerate(videofiles, 1):
                print(f"{idx}. {video}")

            # Selects videos to process
            video_choice = input("Enter the video number(s) to transcribe and generate summary (comma-separated, 0 to go back): ")

            # Ask the user to input the output file name
            output_file_name = input("Enter the desired output file name (without extension): ")
            output_file = f"./learningobjects/{output_file_name}.txt"

            if video_choice == '0':
                continue
            video_numbers = [int(num) for num in video_choice.split(",") if num.isdigit()]
            selected_videos = [videofiles[num - 1] for num in video_numbers if 1 <= num <= len(videofiles)]
            for video_file in selected_videos:
                transcript_file = transcribe_video(video_file)
                generate_summary(transcript_file)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
