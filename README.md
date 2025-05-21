# GPT tutor(FLASK)
해당 저장소는 Flask를 기반으로 음성 인식, GPT 처리, TTS 변환을 통합한 백엔드 서비스입니다. 사용자 음성을 텍스트로 변환한 후 AI 답변을 생성하고 음성 파일로 제공하는 종단간(end-to-end) 처리를 구현했습니다.

프로젝트 개요
gpt_tutor는 음성 기반 AI 튜터 시스템으로 다음과 같은 기술 스택을 사용합니다:

음성 인식: OpenAI Whisper

AI 처리: GPT API

음성 합성: Typecast API

백엔드 프레임워크: Flask

주요 기능 흐름:

사용자 음성 녹음 수신

Whisper를 통한 STT(Speech-to-Text) 변환

GPT API를 이용한 답변 생성

Typecast API로 텍스트→음성 변환

생성된 음성 파일 클라이언트 전송
