# GPT tutor(FLASK)
Flask 기반 음성 AI 튜터 백엔드 서비스

---

## 프로젝트 개요

**gpt_tutor**는 사용자 음성 입력을 받아 Whisper로 텍스트로 변환, GPT API로 답변 생성, Typecast API로 음성 파일로 변환하여 클라이언트에 제공하는 백엔드 서비스입니다.

**주요 기술 스택**
- **음성 인식**: OpenAI Whisper
- **AI 처리**: GPT API
- **음성 합성**: Typecast API
- **백엔드 프레임워크**: Flask

**주요 기능 흐름**
1. **사용자 음성 녹음 수신**
2. **Whisper를 통한 STT(Speech-to-Text) 변환**
3. **GPT API를 이용한 답변 생성**
4. **Typecast API로 텍스트→음성 변환**
5. **생성된 음성 파일 클라이언트 전송**
