#app.py
from flask import Flask
from recording import recording_bp  # recording.py에서 함수 가져오기
from typecast import typecast_bp  # typecast.py에서 함수 가져오기
from gpt import gpt_bp
from typecast_jp import typecastjp_bp
from typecast_en import typecasten_bp

app = Flask(__name__)
app.register_blueprint(recording_bp, url_prefix='/recording')
app.register_blueprint(gpt_bp, url_prefix='/gpt')
app.register_blueprint(typecast_bp, url_prefix='/typecast')
app.register_blueprint(typecastjp_bp, url_prefix='/typecast_jp')
app.register_blueprint(typecasten_bp, url_prefix='/typecast_en')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
