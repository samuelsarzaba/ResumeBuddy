from openai import OpenAI
from time import sleep
import PyPDF2
import sys
import os

client = OpenAI()
starting_assistant = ""
starting_thread = ""


def create_assistant(info):
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            instructions=info,
            name="MyQuickstartAssistant",
            model="gpt-3.5-turbo",
        )
    else:
        my_assistant = client.beta.assistants.retrieve(starting_assistant)

    return my_assistant


def create_thread():
    if starting_thread == "":
        thread = client.beta.threads.create()
    else:
        thread = client.beta.threads.retrieve(starting_thread)

    return thread


def send_message(thread_id, message):
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message


def run_assistant(thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run


def get_newest_message(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data[0]


def get_run_status(thread_id, run_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status


def pdfFunctionality(text):
    my_assistant = create_assistant("Provide resume feedback")
    my_thread = create_thread()
    # latest place with file
    file_path = sys.argv[1]
    user_message = ""
    try:
        with open(file_path, "r") as file:
            user_message += file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found")

    send_message(my_thread.id, text)
    run = run_assistant(my_thread.id, my_assistant.id)
    while run.status != "completed":
        run.status = get_run_status(my_thread.id, run.id)
        sleep(1)
        print("⏳", end="\r", flush=True)
    sleep(0.5)
    response = get_newest_message(my_thread.id)
    print("Response:", response.content[0].text.value)


def ATFFunctionality():
    my_assistant = create_assistant("Extract ATS keywords from this job description")
    my_thread = create_thread()
    # latest place with file
    file_path = sys.argv[1]
    user_message = ""
    try:
        with open(file_path, "r") as file:
            user_message += file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found")

    send_message(my_thread.id, user_message)
    run = run_assistant(my_thread.id, my_assistant.id)
    while run.status != "completed":
        run.status = get_run_status(my_thread.id, run.id)
        sleep(1)
        print("⏳", end="\r", flush=True)
    sleep(0.5)
    response = get_newest_message(my_thread.id)
    print("Response:", response.content[0].text.value)


def main():
    if len(sys.argv) < 2:
        print(
            "Please provide the path to the input text file as a command line argument"
        )
        sys.exit(1)

    choice = input(
        "do you want to use the ATF functionalilty or the PDF functionality? (A/P) "
    )
    if choice == "A" or choice == "a":
        ATFFunctionality()
    if choice == "P" or choice == "p":
        current_file_path = os.path.abspath(__file__)
        with open("./resumes/Redacted Resume 1.pdf", "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                # Extract text from each page
                text += page.extract_text()
        pdfFunctionality(text)


if __name__ == "__main__":
    main()
