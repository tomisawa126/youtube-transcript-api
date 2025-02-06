from flask import Flask, request, jsonify
import yt_dlp
import os
import re

# 🌟 環境変数 COOKIES からデータを取得し、cookies.txt を作成
cookies_content = os.getenv("COOKIES")
if cookies_content:
    with open("cookies.txt", "w") as f:
        f.write(cookies_content)
    print("✅ cookies.txt を作成しました！")
else:
    print("⚠️ 環境変数 COOKIES が設定されていません！")

app = Flask(__name__)

def extract_video_id(url):
    """YouTubeのURLから動画IDを抽出"""
    match = re.search(r"(?:v=|\/|youtu.be\/|embed\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_id, lang="ja"):
    """YouTubeの字幕を取得 (yt-dlp を使用)"""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'writesubtitles': True,
        'subtitleslangs': [lang],
        'subtitlesformat': 'vtt',
        'cookiefile': '/opt/render/project/src/cookies.txt'  # 正しいパスに変更！
        'noplaylist': True,  # プレイリストではなく単一の動画を取得
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            subtitles = info.get('subtitles', {})
            if lang in subtitles:
                transcript_url = subtitles[lang][0]['url']
                return transcript_url  # 字幕のURLを返す
            else:
                return "No subtitles available for this video."
        except yt_dlp.utils.ExtractorError as e:
            return f"ExtractorError: {str(e)}"
        except yt_dlp.utils.DownloadError as e:
            return f"DownloadError: {str(e)}"
        except Exception as e:
            return str(e)

@app.route('/get_transcript', methods=['GET'])
def transcript_api():
    video_id = request.args.get('id')  # 修正: 'url' から 'id' に変更

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    transcript_text = get_transcript(video_id)
    
    if "No subtitles available" in transcript_text or "ExtractorError" in transcript_text or "DownloadError" in transcript_text:
        return jsonify({"error": transcript_text}), 400

    return jsonify({"transcript": transcript_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
