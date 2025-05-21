from openai import OpenAI
import re
import time
from flask import Blueprint, request, jsonify

gpt_bp = Blueprint('gpt', __name__)

Science = 'Asst_API'
Science_check = 'Asst_API'
History = 'Asst_API'
History_check= 'Asst_API'

selected_assistant_id = None

# OpenAi Assistant Ai
client = OpenAI(api_key='MY_API')  


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    return run


def gpt(assistant_ID,transcribed_text):

    assistant = client.beta.assistants.retrieve(assistant_id=assistant_ID)  # Replace with your actual assistant ID
    thread = client.beta.threads.retrieve('thread_qy8Sp2nYOYwVHSPGTmFUtIge')

    print("GPT로 보내는중...")
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=transcribed_text
    )


     # GPT id 매칭
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    wait_on_run(run, thread)

    
    messages = client.beta.threads.messages.list(
        thread_id=thread.id, order="asc", after=message.id
    )


    # 답변 정리(안하면 다른 문자들도 다 딸려옴)
    response_text = ""
    for message in messages:
        for c in message.content:
            response_text += c.text.value
    
    clean_text = re.sub('【.*?】', '', response_text)

    print(f"GPT 답변: {clean_text}")
    

    return clean_text


@gpt_bp.route('/set_assistant', methods=['POST'])
def set_assistant():
    global selected_assistant_id
    data = request.json
    if 'assistant_id' not in data:
        return jsonify({'error': 'No assistant_id provided'}), 400
    
    selected_assistant_id = data['assistant_id']
    return jsonify({'message': 'Assistant ID updated successfully', 'assistant_id': selected_assistant_id}), 200



@gpt_bp.route('/chat', methods=['POST'])
def chat_with_gpt():
    data = request.json
    if 'chat' not in data:
        return jsonify({'error': 'No chat message provided'}), 400

    transcribed_text = data['chat']
    clean_text = gpt(selected_assistant_id, transcribed_text)

    return jsonify({'gpt_response': clean_text}), 200
