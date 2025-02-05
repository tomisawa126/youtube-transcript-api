from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text
    except Exception as e:
        return str(e)

@app.route('/get_transcript', methods=['GET'])
def transcript_api():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    if "youtube.com" in video_url or "youtu.be" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
        transcript_text = get_transcript(video_id)
        return jsonify({"transcript": transcript_text})

    return jsonify({"error": "Invalid YouTube URL"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
