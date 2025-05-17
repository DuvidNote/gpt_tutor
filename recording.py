#recording.py
from openai import OpenAI
from flask import  request, jsonify, Blueprint
import os

recording_bp = Blueprint('recording', __name__)


UPLOADS_DIR = 'uploads'
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


client = OpenAI(api_key='MY_API') 

#녹음 음성 번역
def whisper_trans(file_path, lang):

    print("오디오 번역중...")
    audio_file = open(file_path, "rb")
    transcribed_text = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format = "text",
        language=lang
    )
    print(f"번역된 텍스트: {transcribed_text}")

    return transcribed_text
    


@recording_bp.route('/record', methods=['GET', 'POST'])
def record():
    if 'audio' not in request.files:
        return jsonify({'error': '오디오 파일이 제공되지 않았습니다.'}), 400

    # 업로드된 오디오 파일 저장
    audio_file = request.files['audio']
    file_path = os.path.join(UPLOADS_DIR, audio_file.filename)
    audio_file.save(file_path)

    # Whisper를 사용해 오디오 파일 텍스트 변환 (recording.py)
    transcribed_text = whisper_trans(file_path, 'ko')
    if not transcribed_text:
        return jsonify({'error': '오디오 변환 실패'}), 500
    return jsonify({
        'transcription': transcribed_text
    }), 200

    




@recording_bp.route('/record_jp', methods=['GET', 'POST'])
def record_jp():
    if 'audio' not in request.files:
        return jsonify({'error': '오디오 파일이 제공되지 않았습니다.'}), 400

    # 업로드된 오디오 파일 저장
    audio_file = request.files['audio']
    file_path = os.path.join(UPLOADS_DIR, audio_file.filename)
    audio_file.save(file_path)

    # Whisper를 사용해 오디오 파일 텍스트 변환 (recording.py)
    transcribed_text = whisper_trans(file_path, 'ja')
    if not transcribed_text:
        return jsonify({'error': '오디오 변환 실패'}), 500
    return jsonify({
        'transcription': transcribed_text
    }), 200



@recording_bp.route('/record_en', methods=['GET', 'POST'])
def record_en():
    if 'audio' not in request.files:
        return jsonify({'error': '오디오 파일이 제공되지 않았습니다.'}), 400

    # 업로드된 오디오 파일 저장
    audio_file = request.files['audio']
    file_path = os.path.join(UPLOADS_DIR, audio_file.filename)
    audio_file.save(file_path)

    # Whisper를 사용해 오디오 파일 텍스트 변환 (recording.py)
    transcribed_text = whisper_trans(file_path, 'en')
    if not transcribed_text:
        return jsonify({'error': '오디오 변환 실패'}), 500
    return jsonify({
        'transcription': transcribed_text
    }), 200


