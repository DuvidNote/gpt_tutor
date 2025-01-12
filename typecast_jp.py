#typecast.py
import requests
import json
import time
from flask import Blueprint, jsonify, request, send_file
import os


typecastjp_bp = Blueprint('typecastjp', __name__)


#typecast
url = "https://typecast.ai/api/speak"
API_TOKEN = "Bearer __pltJ9FGBr6yUsD8ekQ9hmjbuAu7JvUZsmEc3Yx5km3N"
HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}


# 1. 모델 설정
def start_speech_synthesis(answer):
    
    payload = {
    "actor_id": "633d5244093ca33db95ddfce",
    "text": answer,
    "lang": "auto",
    "tempo": 1,
    "volume": 100,
    "pitch": 0,
    "xapi_hd": True,
    "max_seconds": 60,
    "model_version": "latest",
    "xapi_audio_format": "wav", 
    "emotion_tone_preset": "toneup-3"
  }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        response_data = json.loads(response.text)
        speak_url = response_data["result"]["speak_url"]
        speak_id = speak_url.split("/")[-1]  # URL의 마지막 부분 추출
        print(f"스피커 ID: {speak_id}")
        return speak_id
    else:
        print(f"에러: {response.status_code}")
        print(response.text)
        return None




# 2. 음성 파일 요청
def poll_synthesis_status(speak_id):
    url = f"https://typecast.ai/api/speak/v2/{speak_id}"
    
    for _ in range(120):  # 120초 동안 요청 반복
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            result = response.json()["result"]
            status = result["status"]
            
            if status == "done":
                audio_url = result["audio_download_url"]
                print(f"Synthesis complete. Audio URL: {audio_url}")
                return audio_url
            elif status == "progress":
                print("Synthesis in progress...")
            else:
                print(f"Unexpected status: {status}")
                break
        else:
            print(f"Error polling synthesis status: {response.status_code}")
            print(response.text)
            break
        
        time.sleep(1)  # 1초 기다리고 다시 반복
    
    return None


# 3. 파일 다운로드
def speaker_audio(speak_url, output_file="castjp.wav"):
    response = requests.get(speak_url)

    
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Audio file downloaded successfully: {output_file}")
    else:
        print(f"Error downloading audio file: {response.status_code}")
        print(response.text)


#음성변환 
def transcribe_and_synthesize(clean_text):
    print("음성 변환중...")
    speak_id = start_speech_synthesis(clean_text)
    
    if speak_id:
        speak_url = poll_synthesis_status(speak_id)
        
        if speak_url:
            speaker_audio(speak_url)
            

    print("음성 저장 성공 'castjp.wav'.")


@typecastjp_bp.route('/download_audio', methods=['GET', 'POST'])
def download_audio():
    # JSON 데이터에서 텍스트 추출
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': '텍스트 데이터가 제공되지 않았습니다.'}), 400

    text = data['text']
    transcribe_and_synthesize(text)  # TTS 변환 함수 호출

    tts_output_path = "castjp.wav"
    if os.path.exists(tts_output_path):
        return send_file(tts_output_path, as_attachment=True)
    else:
        return jsonify({'error': 'Audio file not found'}), 404

