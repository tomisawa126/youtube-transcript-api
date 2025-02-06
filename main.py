from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_transcript(video_id):
    """yt-dlp を使ってYouTube字幕を取得"""
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'subtitleslangs': ['ja', 'en']
        'outtmpl': '%(id)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            if 'requested_subtitles' in info and 'en' in info['requested_subtitles']:
                subtitle_url = info['requested_subtitles']['en']['url']
                return subtitle_url
            else:
                return "No subtitles available."
    except Exception as e:
        return str(e)

@app.route('/get_transcript', methods=['GET'])
def transcript_api():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    transcript_text = get_transcript(video_id)
    
    if "No subtitles available" in transcript_text:
        return jsonify({"error": "Could not retrieve transcript. The video may not have subtitles or is restricted."}), 400

    return jsonify({"transcript": transcript_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
