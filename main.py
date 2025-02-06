from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(url):
    """YouTubeのURLから動画IDを抽出"""
    match = re.search(r"(?:v=|\/|youtu.be\/|embed\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    """YouTube字幕を取得"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text
    except Exception as e:
        return str(e)

@app.route('/get_transcript', methods=['GET'])
def transcript_api():
    video_id = request.args.get('id')  # 修正: 'url' から 'id' に変更

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    transcript_text = get_transcript(video_id)
    
    # YouTubeTranscriptApiがエラーメッセージを返した場合、エラーとして扱う
    if "Could not retrieve" in transcript_text:
        return jsonify({"error": "Could not retrieve transcript. The video may not have subtitles or is restricted."}), 400

    return jsonify({"transcript": transcript_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
